# Appendix C14 - test_doc_operator.py

from klassify.src.doc_operator import DocumentOperator
from klassify.src.db_handler import DBHandler
from klassify.src.tables import Document, Subtopic, Topic
import os
import pytest

database_name = "test_klassify"
if os.path.exists("%s.db" % database_name):
    os.remove("%s.db" % database_name)

def test_docs_with_labels():
    document_1 = Document(title="Test title 1",
                          base_path="/test-1", 
                          content="This is a test document - one")
    document_2 = Document(title="Test title 2",
                          base_path="/test-2", 
                          content="This is a test document - two")

    topic_1 = Topic(
        title='Label 1',
        base_path='/topic/working-sea',
        description='List of information about Topic.'
    )
    topic_2 = Topic(
        title='Label 2',
        base_path='/topic/working-sea-2',
        description='List of information about Topic. 2'
    )

    subtopic_1 = Subtopic(
        title='Subtopic',
        base_path='/topic/working-sea',
        description='List of information about Subtopic.'
    )
    subtopic_2 = Subtopic(
        title='Subtopic 2',
        base_path='/topic/working-sea-2',
        description='List of information about Subtopic. 2'
    )

    topic_1.subtopics = [subtopic_1]
    topic_2.subtopics = [subtopic_2]
    subtopic_1.documents = [document_1]
    subtopic_2.documents = [document_2]

    DBH = DBHandler(db_name=database_name, echo=False)
    session = DBH.session
    session.add_all([topic_1, topic_2, subtopic_1, subtopic_2, document_1, document_2])
    session.commit()

    doc_op = DocumentOperator(db_name = database_name)

    docs_with_labels = doc_op.docs_with_labels
    first_set = docs_with_labels[0]
    second_set = docs_with_labels[1]

    assert [document_1.title, [topic_1.title]] in [[first_set[0].title, first_set[1]], [second_set[0].title, second_set[1]]]
    assert [document_2.title, [topic_2.title]] in [[first_set[0].title, first_set[1]], [second_set[0].title, second_set[1]]]
