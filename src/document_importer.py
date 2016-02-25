import math
from .tables import Subtopic, Document
from .db_handler import DBHandler
import requests
import sqlalchemy

class DocumentImporter(object):

    def __init__(self, db_name="klassify"):
        self.ROOT_URL = "https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING"
        self.PAGE_URL = "https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start="
        self.DBH = DBHandler(db_name)

    def api_response(self, url):
        return requests.get(url).json()

    def total_documents(self, document_data):
        return document_data["total"]

    def pages(self, number_of_documents):
        return math.ceil(number_of_documents / 1000)

    def urls(self, number_of_pages):
        urls = []
        for i in range(number_of_pages):
            item_count = i * 1000
            url_with_pagination = self.PAGE_URL + str(item_count)
            urls.append(url_with_pagination)
        return urls

    def associate_document_with_subtopics(self, document, subtopics):
        # remove duplicates by converting to a set and back to a list
        subtopics = set(subtopics)
        subtopics = list(subtopics)
        document.subtopics = subtopics

        return document

    def make_document(self, document_data):
        link = document_data["link"]
        title = document_data["title"]
        description = document_data["description"]
        doc = Document(
            web_url="https://www.gov.uk" + link,
            description=description,
            base_path=link,
            title=title
        )

        return doc

    def find_subtopics(self, document_data):
        subtopics_data = document_data["specialist_sectors"]

        subtopics = []
        for subtopic_data in subtopics_data:
            subtopic = self.DBH.session.query(Subtopic).filter_by(base_path=subtopic_data['link']).first()

            if subtopic:
                subtopics.append(subtopic)
            # find out what to do when a topic is not found in db
            # maybe create one?

        return subtopics

    def run(self):
        data_response = self.api_response(self.ROOT_URL)
        number_of_documents = self.total_documents(data_response)
        pages = self.pages(number_of_documents)
        urls = self.urls(pages)

        count = 0

        double_documents = []

        for url in urls:
            data_response =  self.api_response(url)
            documents_data = data_response['results']
            for document_data in documents_data:
                document = self.make_document(document_data)
                subtopics = self.find_subtopics(document_data)
                if subtopics:
                    self.associate_document_with_subtopics(document, subtopics)
                # find out what to do when a topic is not found in db
                # maybe create one?

                try:
                    self.DBH.session.add(document)
                    self.DBH.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    double_documents.append(document.base_path)
                    self.DBH.session.rollback()
                except:
                    self.DBH.session.rollback()
                    raise
                print("Item number: ")
                print(count)
                count = count + 1

        self.DBH.session.close()

        print("Documents that appeared twice in the API and have been ignored:")
        print(double_documents)
