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
# add topic to session
# session.add_all([test_topic, test_subtopic])
# commit session to db
# session.commit()

# Example: pull out first subtopic
# session.query(Subtopic).first()

import pdb; pdb.set_trace()
