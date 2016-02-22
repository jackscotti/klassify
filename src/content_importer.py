from .db_handler import DBHandler

from bs4 import BeautifulSoup
import requests

class ContentImporter(object):

    def __init__(self, db_name="klassify"):
        self.DBH = DBHandler(db_name)
        self.session = self.DBH.session
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
        ]

    def parse_page(self, page):
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    def extract_page_content(self, page):
        return page.text

    def documents():
        # read documents from db
        return True

    def build_url(self, document):
        return "https://www.gov.uk" + document.base_path

    def run(self):
        # run importer
        return True

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
