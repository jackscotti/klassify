from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_definition import Topic, Subtopic, Document

engine = create_engine('sqlite:///klassify.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

### Examples:
# create a topic, subtopic and document
# test_topic = Topic(title="HMRC", base_path="/hmrc")
# test_subtopic = Subtopic(title="HMRC payments", base_path="/payments")
# test_document = Document(title="Self assessment deadlines", base_path="/self-assessment", html="<strong>PAY NOW</strong>")

# create relationships
# test_topic.subtopics    = [test_subtopic]
# test_subtopic.documents = [test_document]

# add topic to session
# session.add_all([test_topic, test_subtopic, test_document])

# commit session to db
# session.commit()

### Examples:
# pull out first subtopic
# session.query(Subtopic).first()
# pull out first topic and ask subtopics
# session.query(Topic).first().subtopics
# pull out first document and ask subtopics
# session.query(Document).first().subtopics
# pull out first subtopic and ask documents
# session.query(Subtopic).first().documents

import pdb; pdb.set_trace()
