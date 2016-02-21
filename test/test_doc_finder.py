from klassify.src.tables import Subtopic, Document
from klassify.src.db_handler import DBHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from klassify.src.base import Base
import klassify.src.doc_finder as doc_finder
import json
import subprocess
import os
import pytest
import sqlalchemy

database_name = "test_klassify"
if os.path.exists("%s.db" % database_name):
    os.remove("%s.db" % database_name)

with open('test/fixtures/tagged_documents.json', encoding='utf-8') as fixture_file:
    api_response_fixture = json.loads(fixture_file.read())

DOCUMENT_DATA = api_response_fixture["results"][0]
SUBTOPICS = [
    Subtopic(
        base_path='/topic/driving-tests-and-learning-to-drive/car',
        title='Cars'
    ),
    Subtopic(
        base_path='/topic/driving-tests-and-learning-to-drive/lorry-bus',
        title='Lorries and buses'
    )
]

def test_total_documents():
    assert doc_finder.total_documents(api_response_fixture) == 9623

def test_pages():
    assert doc_finder.pages(9623) == 10

def test_urls():
    assert doc_finder.urls(10) == [
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=0',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=1000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=2000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=3000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=4000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=5000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=6000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=7000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=8000',
        'https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start=9000'
    ]

def test_make_document():
    made_document = doc_finder.make_document(DOCUMENT_DATA)

    assert made_document.web_url == 'https://www.gov.uk/view-driving-licence'
    assert made_document.base_path == '/view-driving-licence'
    assert made_document.title == 'View or share your driving licence information'
    assert made_document.description == 'Find out what information DVLA holds about your driving licence or create a check code to share your driving record (eg to hire a car)'

def test_make_document_subtopics_relationship():
    made_document = doc_finder.make_document(DOCUMENT_DATA)
    doc_finder.make_document_subtopics_relationship(made_document, SUBTOPICS)
    assert made_document.subtopics[0] in SUBTOPICS
    assert made_document.subtopics[1] in SUBTOPICS

def test_find_subtopics():

    DBH = DBHandler(database_name)
    session = DBH.session
    session.add_all(SUBTOPICS)
    session.commit()

    found_topics = doc_finder.find_topics(DOCUMENT_DATA, db_name=database_name)

    subtopics_titles = [subtopic.title for subtopic in SUBTOPICS]
    assert found_topics[0].title in subtopics_titles
    assert found_topics[1].title in subtopics_titles

    DBH.destroy_db_if_present()
