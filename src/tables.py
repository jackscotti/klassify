from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from klassify.src.base import Base

class Topic(Base):
    __tablename__ = 'topics'

    id          = Column(Integer, primary_key=True)
    title       = Column(String)
    base_path   = Column(String, unique=True)
    description = Column(String)
    web_url     = Column(String)
    api_url     = Column(String)

    def __repr__(self):
        return "<User(title='%s', base_path='%s')>" % (self.title, self.base_path)

# create association table (subtopic-documents)
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
        return "<User(title='%s', base_path='%s')>" % (self.title, self.base_path)

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
    api_url     = Column(String)
    html        = Column(Text)
    description = Column(Text)

    subtopics = relationship(
        'Subtopic', secondary=subtopics_documents, back_populates='documents'
    )

    def __init__(self, title, base_path, html=None, description=None, web_url=None, api_url=None):
        self.title       = title
        self.base_path   = base_path
        self.html        = html
        self.web_url     = web_url
        self.api_url     = api_url
        self.description = description

    def __repr__(self):
        return "Document(%r, %r, %r)" % (self.title, self.base_path, self.html)
