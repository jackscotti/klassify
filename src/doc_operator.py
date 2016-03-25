from src.db_handler import DBHandler
from src.tables import Topic, Subtopic, Document
from .word_processor import WordProcessor
import random

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
