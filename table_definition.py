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
    # TODO: add subtopics

    def __repr__(self):
        return "<User(name='%s', slug='%s')>" % (self.name, self.slug)

class Subtopic(Base):
    __tablename__ = 'subtopics'

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    # TODO: add documents

    def __repr__(self):
        return "<User(name='%s', slug='%s')>" % (self.name, self.slug)

# Create tables in database
# always delete db when modifying this
Base.metadata.create_all(engine)
