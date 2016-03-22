from src.db_handler import DBHandler
from src.tables import Topic, Subtopic, Document
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import random

DBH = DBHandler(echo=False)

class WordProcessor():
    def __init__(self, documents):
        self.documents = documents
        self.stemmer = PorterStemmer()
        self.vocabulary = self.make_vocabulary()

    def extract_words(self, document=None):
        '''
        Take all documents content, tokenize it and put it in a `contents` variable
        '''
        if document:
            documents = [document]
        else:
            documents = self.documents

        words = []

        for doc in documents:
            # tokenize
            tokens = word_tokenize(doc.content)

            for token in tokens:
                words.append(token)
        return words

    def downcase_words(self, words):
        return [w.lower() for w in words]

    def remove_stopwords(self, words):
        # remove stop words
        ADDITIONAL_STOP_WORDS = {"-", ".", ",", "if", "good", "what", "within", "https", ".mb"}
        stop_words = set(stopwords.words("english"))
        return [w for w in words if not w in (stop_words | ADDITIONAL_STOP_WORDS)]

    def stem_words(self, words):
        # stem
        return [self.stemmer.stem(w) for w in words]

    def remove_long_words(self, words):
        # remove anything that is not a word (js script that haven't been removed by previous parsing)
        return [w for w in words if len(w) < 25]

    def remove_short_words(self, words):
        filtered_words = []
        for w in words:
            if w.isalpha:
                if len(w) > 1:
                    filtered_words.append(w)
            else:
                filtered_words.append(w)

        return filtered_words

    def make_vocabulary(self, document=None):
        if document:
            v = self.extract_words(document)
        else:
            v = self.extract_words()

        v = self.downcase_words(v)
        v = self.remove_stopwords(v)
        v = self.stem_words(v)
        v = self.remove_short_words(v)
        v = self.remove_long_words(v)

        return v

    def bag_of_words(self, document):
        vocabulary = self.top_words(self.freq_dist(self.vocabulary))

        doc_words = set(self.make_vocabulary(document))
        bag_of_words = {}

        for w in vocabulary:
            bag_of_words[w] = (w in doc_words)

        return bag_of_words

    def freq_dist(self, vocabulary):
        return nltk.FreqDist(vocabulary)

    def top_words(self, freq_dist, number=500):
        return list(freq_dist.keys())[:number]


def random_topics():
    topics = DBH.session.query(Topic).all()
    random.shuffle(topics)
    topics = topics[:3]
    [print(topic.title) for topic in topics]
    return topics

random_topics = random_topics()

def find_documents_for_topic_with_category(topic):
    document_set_with_category = []
    for subtopic in topic.subtopics:
        for document in subtopic.documents:
            document_set_with_category.append([document, topic.title])

    return document_set_with_category

def all_documents():
    documents = []
    for topic in random_topics:
        documents = documents + find_documents_for_topic_with_category(topic)

    return documents

# some docs can appear in several topics, this should not be run
def get_distinct(original_list):
    distinct_list = []
    for each in original_list:
        if each not in distinct_list:
            distinct_list.append(each)
    return distinct_list

document_set_with_category = get_distinct(all_documents())
random.shuffle(document_set_with_category)

# for feeding it to the classifier
# picked_item = document_set_with_category[0]
# document_set_with_category.remove(picked_item)

# remove category
processor = WordProcessor([doc for doc, cat in document_set_with_category])

featuresets = [(processor.bag_of_words(document), category) for (document, category) in document_set_with_category]

class OneVSRest():
    def __init__(self, featuresets, topics):
        self.featuresets = featuresets
        self.topics = topics

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        return featuresets[:half], featuresets[half:]

    def rename_label(self, featureset, topic):
        # Rename to binary labels, Topic VS Rest
        title = topic.title
        if featureset[1] != title:
            featureset = [featureset[0], "Rest"]

        return featureset

    def featuresets_for_one_vs_all(self):
        # Builds a series of binary featureset
        sets_of_featuresets = []

        for topic in self.topics:
            topic_featureset = []
            for featureset in self.featuresets:
                topic_featureset.append(self.rename_label(featureset, topic))
            sets_of_featuresets.append(topic_featureset)

        return sets_of_featuresets

    def sets_of_training_testing_data(self):
        # Split features sets in testing and training sets
        training_testing = []
        for featuresets in self.featuresets_for_one_vs_all():
            training_set, testing_set = self.split_list(featuresets)
            training_testing.append([training_set, testing_set])
        return training_testing


    def train_classifiers(self):
        for training_set, testing_set in self.sets_of_training_testing_data():
            classifier = nltk.NaiveBayesClassifier.train(training_set)

            print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
            for label in classifier.labels():
                if label != "Rest":
                    print("'%s' VS 'Rest':" % label)
            classifier.show_most_informative_features(20)


ovs = OneVSRest(featuresets, random_topics)
ovs.train_classifiers()
