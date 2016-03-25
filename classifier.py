from src.db_handler import DBHandler
from src.tables import Topic, Subtopic, Document
from src.word_processor import WordProcessor

import string
import random
import nltk

class DocumentOperator():
    def __init__(self, n=3):
        self.DBH = DBHandler(echo=False)
        self.topics = self.pick_random_topics(n)
        self.labels = [topic.title for topic in self.topics]
        self.docs_with_labels = self.docs_with_labels()
        print("Topics selected:")
        print(self.labels)
        self.featuresets = []
        self.processor = WordProcessor([doc for doc, cat in self.docs_with_labels])

    def pick_random_topics(self, n):
        topics = self.DBH.session.query(Topic).all()
        random.shuffle(topics)
        topics = topics[:n]
        return topics

    def find_random_doc_by_title(self, title):
        topic = self.DBH.session.query(Topic).filter(Topic.title == title).first()
        subtopic = random.choice(topic.subtopics)
        return random.choice(subtopic.documents)

    def random_document(self):
        all_topics = self.DBH.session.query(Topic).all()
        topic = random.choice(all_topics)
        subtopic = random.choice(topic.subtopics)
        doc = random.choice(subtopic.documents)
        bag_of_words = self.baggify_document(doc)
        return doc, bag_of_words

    def docs_with_labels(self):
        docs_with_labels = []
        for topic in self.topics:
            for subtopic in topic.subtopics:
                for doc in subtopic.documents:
                    doc_labels = self.find_doc_topics(doc)
                    docs_with_labels.append([doc, doc_labels])

        return docs_with_labels

    def find_doc_topics(self, doc):
        labels = []
        for subtopic in doc.subtopics:
            if (subtopic.topic.title in self.labels) and (subtopic.topic.title not in labels):
                labels.append(subtopic.topic.title)
        return labels

    def build_feature_sets(self):
        document_set_with_category = self.docs_with_labels
        random.shuffle(document_set_with_category)

        count = 0
        for (document, category) in document_set_with_category:
            count = count + 1
            if (count % 100 == 0): print("Processing %d of %d" % (count, len(document_set_with_category)))
            self.featuresets.append([self.baggify_document(document), category])

    def baggify_document(self, doc):
        return self.processor.bag_of_words(doc)

doc_op = DocumentOperator()
doc_op.build_feature_sets()
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
            # this raises because of inconsistent shapes, still need to find out why
            import pdb; pdb.set_trace()

    def predict_for_random(self, doc_with_bag_of_words):
        doc, bag_of_words = doc_with_bag_of_words
        print("Predicting for:", doc.title)
        print("Item is labeled to:")
        current_labels = []
        for subtopic in doc.subtopics:
            current_labels.append(subtopic.topic.title)

        print(set(current_labels))

        print("====> Predictions:")

        X = self._vectorizer.fit_transform(bag_of_words)
        predicted_labels = (self.classifier.predict(X))[0]
        probabilities =  self.classifier.predict_proba(X)[0]
        named_classes = self.mlb.classes_

        if not 1 in predicted_labels:
            print("No label suggested for item")
            return

        for idx, label in enumerate(predicted_labels):
            print(named_classes[idx] + " - Confidence: ", end="")
            print(str(round(float(probabilities[idx] * 100), 2)) + "%")

ovs = OvrHandler(doc_op.featuresets)
ovs.train_classifier()
ovs.test_classifier()
import pdb; pdb.set_trace()
ovs.predict_for_random(doc_op.random_document())
