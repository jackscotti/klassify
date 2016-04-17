# Appendix C4 - content_importer.py

from .db_handler import DBHandler
from .tables import Document
from bs4 import BeautifulSoup
import requests
import time

# Future implementation: Tuning features by adding Documents' to their content. Maybe with a multiplier.
class ContentImporter(object):
    def __init__(self, db_name="klassify"):
        self.DBH = DBHandler(db_name, echo=False)
        self.ROOT_URL = "https://www.gov.uk"
        self.NON_RELEVANT_PHRASES = [
            "Skip to main content",
            "Find out more about cookies"
            "GOV.UK uses cookies to make the site simpler",
            "Is there anything wrong with this page",
            "Last updated",
            "Other ways to apply",
            "Before you start",
            "Elsewhere on the web",
            "Find out about call charges",
            "find out more about beta services",
            "Return to top ↑",
            "Find out more about cookies",
            "GOV.UK",
            "Don’t include personal or financial information",
            "Help us improve",
            "This file may not be suitable for users of assistive technology"
            "If you use assistive technology and need a version of this document in a more accessible format",
            "tell us what format you need It will help us if you say what assistive technology you use",
            "Request a different format",
            "What you were doing",
            "What went wrong",
            "uses cookies to make the site simpler."
        ]

    def parse_page(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def extract_page_content(self, page):
        return page.text

    # Iterate through each Document in the database, get their URL on the site and
    # query it to obtain their HTML and eventually store it.
    def import_documents_html(self):
        documents = self.DBH.session.query(Document).all()

        count = 0
        for doc in documents:
            if doc.html == None:
                time.sleep(0.75)
                doc.html = requests.get(doc.web_url).text
                self.DBH.session.commit()
            count += 1
            if count % 250 == 0: print("Documents processed: %d/%d" %(count, len(documents)))

    # Iterate through the Documents' HTML, parse it and store it.
    def extract_documents_content(self):
        documents = self.DBH.session.query(Document).all()

        count = 0
        for doc in documents:
            doc.content = self.extract_content(doc)
            self.DBH.session.commit()
            count += 1
            if count % 250 == 0: print("Documents processed: %d/%d" %(count, len(documents)))

    def extract_content(self, document):
        page = self.parse_page(document.html)
        page = self.remove_unwanted_tags(page)
        page = self.get_body(page)

        page_content = self.extract_page_content(page)
        page_content = self.remove_non_relevant_content(page_content)
        page_content = self.remove_punctuaction_and_numbers(page_content)
        return page_content

    def get_body(self, page):
        return page.body

    # Discard anything inside footer, header and scripts
    def remove_unwanted_tags(self, page):
        for tag in page.find_all(['footer', 'script', 'header']):
            tag.replace_with('')

        return page

    def remove_non_relevant_content(self, page):
        for phrase in self.NON_RELEVANT_PHRASES:
            page = page.replace(phrase, "")
        return page

    def remove_punctuaction_and_numbers(self, page):
        punctuation = [ '\\', '>', '_', '`', '{', ']', '*', '[',
                        '^', '+', '!', '(', ':', ';', "'", "’",
                        '<', '|', '"', '?', '=', '}', '&', '/',
                        '$', ')', '~', '#', '%', ',' ]
        page = ''.join(ch for ch in page if ch not in punctuation)
        page = ''.join([i for i in page if not i.isdigit()])
        return page
