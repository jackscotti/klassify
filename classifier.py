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
    topics = topics[:4]
    print("Topics selected:")
    print([topic.title for topic in topics])
    return topics

def find_documents_for_topic_with_category(topic):
    document_set_with_category = []
    for subtopic in topic.subtopics:
        for document in subtopic.documents:
            document_subtopics = document.subtopics
            document_topics = [subtopic.topic.title for subtopic in document_subtopics]
            labels = []
            for document_topic in document_topics:
                if document_topic in selected_labels and document_topic not in labels:
                    labels.append(document_topic)

            document_set_with_category.append([document, labels])

    return document_set_with_category

def all_documents():
    documents = []
    for topic in random_topics:
        documents = documents + find_documents_for_topic_with_category(topic)

    return documents

def find_random_doc_by_title(title):
    topic = DBH.session.query(Topic).filter(Topic.title == title).first()
    subtopic = random.choice(topic.subtopics)
    return random.choice(subtopic.documents)

def random_document():
    topics = DBH.session.query(Topic).all()
    topic = random.choice(topics)
    subtopic = random.choice(topic.subtopics)
    return random.choice(subtopic.documents)

DBH = DBHandler(echo=False)
random_topics = random_topics()
selected_labels = [topic.title for topic in random_topics]

document_set_with_category = all_documents()
random.shuffle(document_set_with_category)

# remove category
processor = WordProcessor([doc for doc, cat in document_set_with_category])

featuresets = []
count = 0
for (document, category) in document_set_with_category:
    count = count + 1
    if (count % 100 == 0): print("Processing %d of %d" % (count, len(document_set_with_category)))
    featuresets.append([processor.bag_of_words(document), category])

# from sklearn.naive_bayes import GaussianNB
# from sklearn.naive_bayes import BernoulliNB
from nltk import compat
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import DictVectorizer

class OvrHandler():
    def __init__(self, featuresets):
        self.mlb = MultiLabelBinarizer()
        self.training_featuresets, self.testing_sets = self.split_list(featuresets)
        self._vectorizer = DictVectorizer(dtype=float, sparse=True)
        self.classifier = OneVsRestClassifier(MultinomialNB())

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        return featuresets[:half], featuresets[half:]

    def prepare_scikit_x_and_y(self, labeled_featuresets):
        X, y = list(compat.izip(*labeled_featuresets))
        X = self._vectorizer.fit_transform(X)

        set_of_labels = []
        for label in y:
            set_of_labels.append(set(label))

        y = self.mlb.fit_transform(set_of_labels)

        return X, y

    def train_classifier(self):
        X, y = self.prepare_scikit_x_and_y(self.training_featuresets)
        self.classifier.fit(X, y)

    def test_classifier(self):
        try:
          X, y = self.prepare_scikit_x_and_y(self.testing_sets)
          print("Classifier accuracy against test data:", str(round(float(self.classifier.score(X, y) * 100), 2)) + "%")
        except Exception:
          import pdb; pdb.set_trace()

    def predict_for_random(self, doc):
        print("Predicting for:", doc.title)
        print("Item is labeled to:")
        current_labels = []
        for subtopic in doc.subtopics:
            current_labels.append(subtopic.topic.title)

        print(set(current_labels))

        print("====> Predictions:")

        X = self._vectorizer.fit_transform(processor.bag_of_words(doc))
        predicted_labels = (self.classifier.predict(X))[0]
        probabilities =  self.classifier.predict_proba(X)[0]
        named_classes = self.mlb.classes_

        if not 1 in predicted_labels:
            print("No label suggested for item")
            return

        for idx, label in enumerate(predicted_labels):
            print(named_classes[idx] + " - Confidence: ", end="")
            print(str(round(float(probabilities[idx] * 100), 2)) + "%")

ovs = OvrHandler(featuresets)
ovs.train_classifier()
ovs.test_classifier()
ovs.predict_for_random(random_document())

# TODO: now i can set documents with multiple topics, remove duplicates
