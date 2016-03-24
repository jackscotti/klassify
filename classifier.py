from src.db_handler import DBHandler
from src.tables import Topic, Subtopic, Document
from src.word_processor import WordProcessor

import string
import random
import pickle
import nltk

DBH = DBHandler(echo=False)

def random_topics():
    topics = DBH.session.query(Topic).all()
    random.shuffle(topics)
    topics = topics[:3]
    print("Topics selected:")
    print([topic.title for topic in topics])
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

document_set_with_category = all_documents()

random.shuffle(document_set_with_category)

# remove category
processor = WordProcessor([doc for doc, cat in document_set_with_category])

featuresets = []
count = 0
for (document, category) in document_set_with_category:
    count = count + 1
    if (count % 25 == 0): print("Processing %d of %d" % (count, len(document_set_with_category)))
    featuresets.append([processor.bag_of_words(document), category])


from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
# from sklearn.naive_bayes import GaussianNB
# from sklearn.naive_bayes import BernoulliNB
from sklearn.multiclass import OneVsRestClassifier
from nltk import compat

from sklearn.preprocessing import MultiLabelBinarizer

class OneVSRest():
    def __init__(self, featuresets, topics):
        self.featuresets = featuresets[:100]
        self.topics = topics

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        return featuresets[:half], featuresets[half:]

    # def train_classifiers(self):
    #     training_set, testing_set = self.split_list(self.featuresets)
    #
    #     ovr = SklearnClassifier(OneVsRestClassifier(MultinomialNB()))
    #     # ovr.train(training_set)
    #     #
    #     # print("One-vs-rest accuracy percent:",(nltk.classify.accuracy(ovr, testing_set))*100)
    #     #
    #     # self.classifier = ovr

    def build_classifier(self):

        ovr = SklearnClassifier(OneVsRestClassifier(MultinomialNB()))

        self.classifier = ovr

    def train_classifier(self):
        labeled_featuresets, testing_set = self.split_list(self.featuresets)

        X, y = list(compat.izip(*labeled_featuresets))
        import pdb; pdb.set_trace()
        X = self.classifier._vectorizer.fit_transform(X)
        y = self.classifier._encoder.fit_transform(y)

        mlb = MultiLabelBinarizer()

        self.classifier._clf.fit(X, y)

        print("One-vs-rest accuracy percent:",(nltk.classify.accuracy(self.classifier, testing_set))*100)

        return self.classifier

    def classify_single_document(self, document):
        bag_of_words = processor.bag_of_words(document)

        for label in self.classifier.labels():
            probability = self.classifier.prob_classify(bag_of_words).prob(label) * 100
            probability = round(probability, 2)
            print("Label: %s" % label)
            print("-> confidence: " +  str(probability) + "%")

        print("\nDoc data:")
        print(document.web_url)
        for subtopic in document.subtopics:
            print("Topic: %s" % subtopic.topic.title)

ovs = OneVSRest(featuresets, random_topics)
ovs.build_classifier()
ovs.train_classifier()

def find_random_doc_by_title(title):
    topic = DBH.session.query(Topic).filter(Topic.title == title).first()
    subtopic = random.choice(topic.subtopics)
    return random.choice(subtopic.documents)

def random_document():
    topics = DBH.session.query(Topic).all()
    topic = random.choice(topics)
    subtopic = random.choice(topic.subtopics)
    return random.choice(subtopic.documents)

import pdb; pdb.set_trace()
ovs.classify_single_document(random_document())
