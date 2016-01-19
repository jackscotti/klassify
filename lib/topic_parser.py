import requests

BASE_URL = 'https://www.gov.uk/api/content'
TOPICS_PATH = '/topic'

home = requests.get(BASE_URL + TOPICS_PATH).json()

topics = home['links']['children']

topics_with_subtopics = []

print("Topic,Subtopic")
for topic in topics:
    topic_base_path = topic['base_path']

    topic = requests.get(BASE_URL + topic_base_path).json()

    subtopics = topic['links']['children']

    for subtopic in subtopics:
        subtopic_base_path = subtopic["base_path"]
        print(topic_base_path + "," + subtopic_base_path)

'''
Spreadsheet:
https://docs.google.com/spreadsheets/d/1PtgivxT7aCrmgogS7yV2nEPlK12hkkTSzKMFwA-_k1I
'''
