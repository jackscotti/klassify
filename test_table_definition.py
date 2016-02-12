from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_definition import Topic, Subtopic, Document
import subprocess
import os

database_name = "test_klassify"

subprocess.call("python3 table_definition.py %s" % database_name, shell=True)
engine = create_engine("sqlite:///%s.db" % database_name, echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

def test_db():
    # create a topic, subtopic and document
    test_topic = Topic(title="HMRC", base_path="/hmrc")
    test_subtopic_1 = Subtopic(title="HMRC payments", base_path="/payments")
    test_subtopic_2 = Subtopic(title="HMRC refunds", base_path="/refunds")
    test_document_1 = Document(title="Self assessment deadlines", base_path="/self-assessment", html="<strong>PAY NOW</strong>")
    test_document_2 = Document(title="Starting a business", base_path="/start-business", html="<strong>START NOW</strong>")
    test_document_3 = Document(title="Payment and refunds", base_path="/payments-and-refunds", html="<h1>payments and refunds</h1>")

    # create relationships
    test_topic.subtopics    = [test_subtopic_1, test_subtopic_2]
    test_subtopic_1.documents = [test_document_1, test_document_2]
    test_document_3.subtopics = [test_subtopic_1, test_subtopic_2]

    # add topic to session
    session.add_all([
        test_topic,
        test_subtopic_1,
        test_subtopic_2,
        test_document_1,
        test_document_2,
        test_document_3
    ])

    # Table properties
    assert session.query(Topic).first().title == test_topic.title
    assert session.query(Topic).first().base_path == test_topic.base_path
    assert session.query(Subtopic).first().title == test_subtopic_1.title
    assert session.query(Subtopic).first().base_path == test_subtopic_1.base_path
    assert session.query(Document).first().title == test_document_1.title
    assert session.query(Document).first().base_path == test_document_1.base_path

    # test relationships
    db_subtopics = session.query(Topic).first().subtopics
    assert db_subtopics[0].title == test_subtopic_1.title
    assert db_subtopics[1].title == test_subtopic_2.title

    db_documents = session.query(Subtopic).first().documents
    assert db_documents[0].title == test_document_1.title
    assert db_documents[1].title == test_document_2.title

    last_document_subtopics = session.query(Document).order_by(Document.id.desc()).first().subtopics
    assert last_document_subtopics[0].title == test_subtopic_1.title
    assert last_document_subtopics[1].title == test_subtopic_2.title

    # terminate session and delete test db
    session.close()
    os.remove("%s.db" % database_name)
