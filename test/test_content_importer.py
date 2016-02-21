from klassify.src.tables import Document
from klassify.src.content_importer import ContentImporter
import os
import pytest
import sqlalchemy
import requests
# necessary for mocking requests
import responses

database_name = "test_klassify"

if os.path.exists("%s.db" % database_name):
    os.remove("%s.db" % database_name)

DOCUMENT = Document(
    base_path="/intelligent-machines",
    title="The Intelligent Machines"
)

IMPORTER = ContentImporter(db_name=database_name)
DOCUMENT_HTML = open("test/fixtures/document_page.html", 'r')

@responses.activate
def test_extract_content():

    responses.add(responses.GET, 'https://www.gov.uk/government/organisations/hm-revenue-customs',
    body=DOCUMENT_HTML.read(), status=200,
    content_type='application/html')

    page = requests.get('https://www.gov.uk/government/organisations/hm-revenue-customs')

    page = IMPORTER.parse_page(page)

    STRING_PRESENT_IN_BOTH_HEADER_AND_FOOTER = "How government works"
    assert STRING_PRESENT_IN_BOTH_HEADER_AND_FOOTER in page.text
    page = IMPORTER.remove_footer(page)
    page = IMPORTER.remove_header(page)
    assert STRING_PRESENT_IN_BOTH_HEADER_AND_FOOTER not in page.text

    STRING_PRESENT_IN_SCRIPT_TAG = "<![CDATA["
    assert STRING_PRESENT_IN_SCRIPT_TAG in page.text
    page = IMPORTER.remove_script_tags(page)
    assert STRING_PRESENT_IN_SCRIPT_TAG not in page.text

    STRING_PRESENT_IN_TITLE = "HM Revenue & Customs"
    assert STRING_PRESENT_IN_TITLE in page.text
    page = IMPORTER.get_body(page)
    assert STRING_PRESENT_IN_TITLE not in page.text

    page_content = IMPORTER.extract_page_content(page)

    assert "\n" in page_content
    page_content = IMPORTER.strip_new_lines(page_content)
    assert "\n" not in page_content

    import pdb; pdb.set_trace()
