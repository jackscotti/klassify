from src.db_handler import DBHandler
from src.tables import Topic, Subtopic, Document
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

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
        ADDITIONAL_STOP_WORDS = {"-", ".", ",", "if", "good", "what", "within", "https"}
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



topics = DBH.session.query(Topic).all()

# to make things quick
topics = [topics[0], topics[20]]

document_set_with_category = []
def find_documents_for_topic_with_category(topic):
    documents = []
    for subtopic in topic.subtopics:
        for document in subtopic.documents:
            document_set_with_category.append([document, topic.title])


for topic in topics:
    find_documents_for_topic_with_category(topic)


def get_distinct(original_list):
    distinct_list = []
    for each in original_list:
        if each not in distinct_list:
            distinct_list.append(each)
    return distinct_list

# import pdb; pdb.set_trace()
document_set_with_category = get_distinct(document_set_with_category)
picked_item = document_set_with_category[:1]
document_set_with_category.remove(picked_item[0])

document_set = []
# import pdb; pdb.set_trace()
for doc, cat in document_set_with_category:
    document_set.append(doc)

# import pdb; pdb.set_trace()
processor = WordProcessor(document_set)

import random
random.shuffle(document_set_with_category)

featuresets = [(processor.bag_of_words(document), category) for (document, category) in document_set_with_category]
for f, c in featuresets:
    print(c)

def split_list(featuresets):
    half = int(len(featuresets)/2)
    return featuresets[:half], featuresets[half:]

training_set, testing_set  = split_list(featuresets)

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)
