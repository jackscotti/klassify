from klassify.src.table_definition import Subtopic, Document
import klassify.src.doc_finder as doc_finder
import json

with open('test/fixtures/tagged_documents.json', encoding='utf-8') as fixture_file:
    api_response_fixture = json.loads(fixture_file.read())

def document_data():
    return api_response_fixture["results"][0]

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
    made_document = doc_finder.make_document(document_data())

    assert made_document.web_url == 'https://www.gov.uk/view-driving-licence'
    assert made_document.base_path == '/view-driving-licence'
    assert made_document.title == 'View or share your driving licence information'
    assert made_document.description == 'Find out what information DVLA holds about your driving licence or create a check code to share your driving record (eg to hire a car)'
