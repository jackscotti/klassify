# iterate through topics
# iterate through subtopics
# iterate through documents
# get rendering app
# <meta name="govuk:rendering-application" content="whitehall">


'''
TODO:
Generate CSV output with headers:
slug,topics,subtopic,url,document_type,rendering app
'''

import requests

def subtopic_slug(subtopic):
    return subtopic[7:]

BASE_URL = 'https://www.gov.uk'
API_BASE_URL = 'https://www.gov.uk/api/content'
TOPICS_PATH = '/topic'
SEARCH_BASE_URL = 'https://www.gov.uk/api/search.json?filter_specialist_sectors='
HEADERS = "topic,subtopic,document_url,document_type"

home = requests.get(API_BASE_URL + TOPICS_PATH).json()
topics = home['links']['children'][:2]

topics_with_subtopics = []

print(HEADERS)

for topic in topics:
    topic_base_path = topic['base_path']

    topic = requests.get(API_BASE_URL + topic_base_path).json()

    subtopics = topic['links']['children'][:2]

    for subtopic in subtopics:
        subtopic_base_path = subtopic["base_path"]

        # for debugging, what I'm querying
        # print(SEARCH_BASE_URL + subtopic_slug(subtopic_base_path))

        tagged_docs = requests.get(SEARCH_BASE_URL + subtopic_slug(subtopic_base_path)).json()

        docs = tagged_docs["results"]
        for doc in docs:
            print(topic_base_path + "," + subtopic_base_path + "," + BASE_URL + doc["link"] + "," + doc["document_type"])
