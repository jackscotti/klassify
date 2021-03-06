# Appendix C10 - tables.py

from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from .base import Base

class Topic(Base):
    __tablename__ = 'topics'

    id          = Column(Integer, primary_key=True)
    title       = Column(String)
    base_path   = Column(String, unique=True)
    description = Column(String)
    web_url     = Column(String)
    api_url     = Column(String)

    def __repr__(self):
        return "<Topic(title='%s', base_path='%s')>" % (self.title, self.base_path)

    def documents(self):
        documents = set()
        for subtopic in self.subtopics:
            for doc in subtopic.documents:
                documents.add(doc)

        return list(documents)

    def documents_with_labels(self):
        doc_with_labels = []
        for doc in self.documents():
            doc_with_labels.append([doc, doc.topic_titles()])
        return doc_with_labels

# create association table SubtopicDcoument
subtopics_documents = Table('subtopics_documents', Base.metadata,
    Column('subtopic_id', ForeignKey('subtopics.id'), primary_key=True),
    Column('document_id', ForeignKey('documents.id'), primary_key=True)
)

class Subtopic(Base):
    __tablename__ = 'subtopics'

    id          = Column(Integer, primary_key=True)
    title       = Column(String)
    base_path   = Column(String, unique=True)
    description = Column(String)
    web_url     = Column(String)
    api_url     = Column(String)

    topic_id  = Column(Integer, ForeignKey('topics.id'))
    topic     = relationship("Topic", back_populates="subtopics")

    documents = relationship(
        "Document", secondary=subtopics_documents, back_populates="subtopics"
    )

    def __repr__(self):
        return "<Subtopic(title='%s', base_path='%s')>" % (self.title, self.base_path)

# link topic to subtopics
Topic.subtopics = relationship(
    "Subtopic", order_by=Subtopic.id, back_populates="topic"
)

class Document(Base):
    __tablename__ = 'documents'

    id          = Column(Integer, primary_key=True)
    title       = Column(String)
    base_path   = Column(String, unique=True)
    web_url     = Column(String)
    html        = Column(Text)
    description = Column(Text)
    content     = Column(Text)

    subtopics = relationship(
        'Subtopic', secondary=subtopics_documents, back_populates='documents'
    )

    def __init__(self, title, base_path, html=None, description=None, web_url=None, content=None):
        self.title       = title
        self.base_path   = base_path
        self.html        = html
        self.web_url     = web_url
        self.description = description
        self.content     = content

    def __repr__(self):
        return "<Document(title=%r, base_path=%r)" % (self.title, self.base_path)

    def topics(self):
        topics = set()

        for subtopic in self.subtopics:
            topics.add(subtopic.topic)

        return list(topics)

    def topic_titles(self):
        return [topic.title for topic in self.topics()]
