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

class Subtopic(Base):
    __tablename__ = 'subtopics'

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    topic = relationship("Topic", back_populates="subtopics")


    def __repr__(self):
        return "<User(name='%s', slug='%s')>" % (self.name, self.slug)

# link topic to subtopics
Topic.subtopics = relationship(
    "Subtopic", order_by=Subtopic.id, back_populates="topic"
)
# Create tables in database
# always delete db when modifying this
Base.metadata.create_all(engine)
