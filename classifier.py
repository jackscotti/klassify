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
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.multiclass import OneVsRestClassifier

class OneVSRest():
    def __init__(self, featuresets, topics):
        self.featuresets = featuresets
        self.topics = topics
        self.classifiers = []

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        return featuresets[:half], featuresets[half:]

    def train_classifiers(self):
        training_set, testing_set = self.split_list(self.featuresets)

        one_vs_rest = SklearnClassifier(OneVsRestClassifier(MultinomialNB()))

        one_vs_rest.train(training_set)

        print("One-vs-rest accuracy percent:",(nltk.classify.accuracy(one_vs_rest, testing_set))*100)

        self.classifier = one_vs_rest

    def classify_single_document(self, document):
        bag_of_words = processor.bag_of_words(document)

        for label in self.classifier.labels():
            probability = self.classifier.prob_classify(bag_of_words).prob(label) * 100
            probability = round(probability, 2)
            print("Doc is: %s" % label)
            print("-> confidence: " +  str(probability) + "%")

        print("\nDoc data:")
        print(document.web_url)
        for subtopic in document.subtopics:
            print("Topic: %s" % subtopic.topic.title)


ovs = OneVSRest(featuresets, random_topics)
ovs.train_classifiers()

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
