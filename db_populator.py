from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_definition import Topic, Subtopic

engine = create_engine('sqlite:///klassify.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Examples:
# create a topic
# test_topic = Topic(name="HMRC", slug="/hmrc")
# create a subtopic
# test_subtopic = Subtopic(name="HMRC payments", slug="/payments")

# add subtopic to topic
# test_topic.subtopics = [test_subtopic]

# add topic to session
# session.add_all([test_topic, test_subtopic])

# commit session to db
# session.commit()

# Example: pull out first subtopic
# session.query(Subtopic).first()
# Example: pull out first topic and ask subtopics
# session.query(Topic).first().subtopics

import pdb; pdb.set_trace()
