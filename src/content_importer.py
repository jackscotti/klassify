from .db_handler import DBHandler
from .tables import Document
from bs4 import BeautifulSoup
import requests
import time


class ContentImporter(object):

    def __init__(self, db_name="klassify"):
        self.DBH = DBHandler(db_name)
        self.ROOT_URL = "https://www.gov.uk"
        self.NON_RELEVANT_PHRASES = [
            "Skip to main content",
            "GOV.UK uses cookies to make the site simpler.",
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
            "Beta",
            "GOV.UK",
        ]

    def parse_page(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def extract_page_content(self, page):
        return page.text

    def import_documents_html(self):
        documents = self.DBH.session.query(Document).all()
        count = len(documents)

        for doc in documents:
            if doc.html == None:
                time.sleep(0.20)
                doc.html = requests.get(doc.web_url).text
                self.DBH.session.commit()
            print(doc.web_url)
            count = count - 1
            print("Documents left: %s" % count)

    def import_documents_content(self):
        documents = self.DBH.session.query(Document).all()
        count = len(documents)

        for doc in documents:
            if doc.content == None:
                doc.content = self.extract_content(doc)
                self.DBH.session.commit()
            print(doc.web_url)
            count = count - 1
            print("Documents left: %s" % count)

    def extract_content(self, document):
        page = self.parse_page(document.html)
        page = self.remove_footer(page)
        page = self.remove_header(page)
        page = self.remove_script_tags(page)
        page = self.get_body(page)

        page_content = self.extract_page_content(page)
        page_content = self.strip_new_lines(page_content)
        page_content = self.remove_non_relevant_content(page_content)
        return page_content

    def strip_new_lines(self, page):
        return page.replace('\n', ' ')

    def get_body(self, page):
        return page.body

    def remove_footer(self, page):
        # Discard anything inside<footer></footer>
        [s.extract() for s in page('footer')]
        return page

    def remove_script_tags(self, page):
        # Discard anything inside <script></script>
        [s.extract() for s in page('script')]
        return page

    def remove_header(self, page):
        # Discard anything inside <header></header>
        [s.extract() for s in page('header')]
        return page

    def remove_non_relevant_content(self, page):
        for phrase in self.NON_RELEVANT_PHRASES:
            page = page.replace(phrase, "")
        return page

    def remove_punctuaction_and_numbers(self, page):
        punctuation = ['\\', '>', '@', '_', '`', '{', ']', '*', '[', '^', '+', '!', '(', ':', ';', "'", '<', '|', '"', '?', '=', '}', '&', '/', '$', ')', '.', '~', '#', '%', ',']

        page = ''.join(ch for ch in page if ch not in punctuation)
        page = ''.join([i for i in page if not i.isdigit()])
        
        return page
