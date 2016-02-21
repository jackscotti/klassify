# TODO: rename file

import requests
import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from klassify.src.tables import Subtopic, Document
from klassify.src.db_handler import DBHandler

ROOT_URL = "https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING"
PAGE_URL = "https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING&count=1000&start="

def response():
    response = requests.get(ROOT_URL).json()

def total_documents(document_data):
    return document_data["total"]

def pages(number_of_documents):
    return math.ceil(number_of_documents / 1000)

def urls(number_of_pages):
    urls = []
    for i in range(number_of_pages):
        item_count = i * 1000
        url_with_pagination = PAGE_URL + str(item_count)
        urls.append(url_with_pagination)
    return urls

def associate_document_with_subtopics(doc, subtopics):
    doc.subtopics = subtopics


def make_document(document_data):
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

def make_document_subtopics_relationship(document, subtopics):
    document.subtopics = subtopics
    return document


def find_topics(document_data, db_name='klassify'):
    DBH = DBHandler(db_name)
    session = DBH.session
    subtopics_data = document_data["specialist_sectors"]
    subtopics = []

    for subtopic_data in subtopics_data:
        subtopics.append(session.query(Subtopic).filter_by(base_path=subtopic_data['link']).first())

    return subtopics

def run():
    for url in urls():
        response = requests.get(url).json()
        results = response["results"]
        for result in results:

# for each page, create a document with its subtopics and store
# specialist_sectors: [
# {
# title: "Cars",
# slug: "driving-tests-and-learning-to-drive/car",
# link: "/topic/driving-tests-and-learning-to-drive/car"
# }