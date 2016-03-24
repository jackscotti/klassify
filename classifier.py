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
    if (count % 50 == 0): print("Processing %d of %d" % (count, len(document_set_with_category)))
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
        self.topics = topics
        self.mlb = MultiLabelBinarizer()
        # labeled_featuresets should become training featuresets
        self.training_featuresets, self.testing_sets = self.split_list(featuresets)

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        return featuresets[:half], featuresets[half:]

    def build_classifier(self):
        self.classifier = SklearnClassifier(OneVsRestClassifier(MultinomialNB()))

    def prepare_scikit_x_and_y(self, labeled_featuresets):
        X, y = list(compat.izip(*labeled_featuresets))
        X = self.classifier._vectorizer.fit_transform(X)

        set_of_labels = []
        for label in y:
            set_of_labels.append(set([label]))

        y = self.mlb.fit_transform(set_of_labels)

        return X, y

    def train_classifier(self):
        X, y = self.prepare_scikit_x_and_y(self.training_featuresets)
        self.classifier._clf.fit(X, y)

    def test_classifier(self):
        X, y = self.prepare_scikit_x_and_y(self.testing_sets)
        print("Classifier accuracy against test data:", str(round(float(self.classifier._clf.score(X, y) * 100), 2)) + "%")

    def predict_for_random(self, doc):
        print("Predicting for:", doc.title)
        print("Item is labeled to:")
        current_labels = []
        for subtopic in doc.subtopics:
            current_labels.append(subtopic.topic.title)

        # import pdb; pdb.set_trace()
        print(set(current_labels))

        print("====> Predictions:")

        X = self.classifier._vectorizer.fit_transform(processor.bag_of_words(doc))
        predicted_labels = (self.classifier._clf.predict(X))[0]
        probabilities =  self.classifier._clf.predict_proba(X)[0]
        named_classes = self.mlb.classes_

        if not 1 in predicted_labels:
            print("No label suggested for item")
            return

        for idx, label in enumerate(predicted_labels):
            # import pdb; pdb.set_trace()
            print(named_classes[idx] + " - Confidence: ", end="")
            print(str(round(float(probabilities[idx] * 100), 2)) + "%")

ovs = OneVSRest(featuresets, random_topics)
ovs.build_classifier()
ovs.train_classifier()
ovs.test_classifier()

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
ovs.predict_for_random(random_document())

# now i can set documents with multiple topics, remove duplicates
