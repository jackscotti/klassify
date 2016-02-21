from .db_handler import DBHandler

from bs4 import BeautifulSoup
import requests

class ContentImporter(object):

    def __init__(self, db_name="klassify"):
        self.DBH = DBHandler(db_name)
        self.session = self.DBH.session
        self.ROOT_URL = "https://www.gov.uk"

    def parse_page(self, page):
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    def extract_page_content(self, page):
        return page.text

    def documents():
        # read documents from db
        return True

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

# TODO:
# Remove:
#     <div id="skiplink-container">
#       <div>
#         <a href="#content" class="skiplink">Skip to main content</a>
#       </div>
#     </div>
#
#     <div id="global-cookie-message">
#         <p>GOV.UK uses cookies to make the site simpler. <a href="https://www.gov.uk/help/cookies">Find out more about cookies</a></p>
#     </div>
