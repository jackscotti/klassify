from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///klassify.db', echo=True)
Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topics'

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)

    def __repr__(self):
        return "<User(name='%s', slug='%s')>" % (self.name, self.slug)

# create association table (subtopic-documents)
subtopics_documents = Table('subtopics_documents', Base.metadata,
    Column('subtopic_id', ForeignKey('subtopics.id'), primary_key=True),
    Column('document_id', ForeignKey('documents.id'), primary_key=True)
)

class Subtopic(Base):
    __tablename__ = 'subtopics'

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)

    topic_id  = Column(Integer, ForeignKey('topics.id'))
    topic     = relationship("Topic", back_populates="subtopics")

    documents = relationship(
        "Document", secondary=subtopics_documents, back_populates="subtopics"
    )

    def __repr__(self):
        return "<User(name='%s', slug='%s')>" % (self.name, self.slug)

# link topic to subtopics
Topic.subtopics = relationship(
    "Subtopic", order_by=Subtopic.id, back_populates="topic"
)

class Document(Base):
    __tablename__ = 'documents'

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    html = Column(Text)

    subtopics = relationship(
        'Subtopic', secondary=subtopics_documents, back_populates='documents'
    )

    def __init__(self, name, slug, html):
        self.name = name
        self.slug = slug
        self.html = html

    def __repr__(self):
        return "Document(%r, %r, %r)" % (self.name, self.slug, self.html)

# Create tables in database
# always delete db when modifying this
Base.metadata.create_all(engine)
