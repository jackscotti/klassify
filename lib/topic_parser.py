'''
Generate CSV-like output with headers:
Topic,Subtopic,Total tagged to subtopic
'''

import requests

def subtopic_slug(subtopic):
    return subtopic[7:]

BASE_URL = 'https://www.gov.uk/api/content'
TOPICS_PATH = '/topic'
SEARCH_BASE_URL = 'https://www.gov.uk/api/search.json?filter_specialist_sectors='

home = requests.get(BASE_URL + TOPICS_PATH).json()

topics = home['links']['children']

topics_with_subtopics = []

print("Topic,Subtopic,Total tagged to subtopic")
for topic in topics:
    topic_base_path = topic['base_path']

    topic = requests.get(BASE_URL + topic_base_path).json()

    subtopics = topic['links']['children']

    for subtopic in subtopics:
        subtopic_base_path = subtopic["base_path"]

        tagged_docs = requests.get(SEARCH_BASE_URL + subtopic_slug(subtopic_base_path)).json()
        total_tagged_docs = tagged_docs["total"]

        print(topic_base_path + "," + subtopic_base_path + "," + str(total_tagged_docs))
