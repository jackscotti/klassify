import requests

BASE_URL = 'https://www.gov.uk/api/content'
TOPICS_PATH = '/topic'

home = requests.get(BASE_URL + TOPICS_PATH).json()

topics = home['links']['children']

topics_with_subtopics = []
for topic in topics:
    base_path = topic['base_path']

    print("Querying: " + BASE_URL + base_path)
    topic = requests.get(BASE_URL + base_path).json()

    subtopics = topic['links']['children']
    topic['subtopics'] = subtopics
    topics_with_subtopics.append(topic)

print(topics_with_subtopics)
