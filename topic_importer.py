# Loop through topics
# Loops through subtopics
# Assign them to their parents
# Save all
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_definition import Topic, Subtopic

engine = create_engine('sqlite:///klassify.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

API_URL = "https://www.gov.uk/api/content"
root = requests.get(API_URL + "/topic").json()

topics = root["links"]["children"]

for topic in topics:
    "TO COMPLETE"
    topic_base_path = topic["base_path"]
    subtopics = requests.get(API_URL + topic_base_path).json()
    subtopics = subtopics["links"]["children"]

def make_topic_model(topic_data):
    return Topic(
        title=topic_data["title"],
        base_path=topic_data["base_path"],
        web_url=topic_data["web_url"],
        api_url=topic_data["api_url"],
        description=topic_data["description"]
    )

def make_subtopic_model(subtopic_data):
    return Subtopic(
        title=topic_data["title"],
        base_path=topic_data["base_path"],
        web_url=topic_data["web_url"],
        api_url=topic_data["api_url"],
        description=topic_data["description"]
    )

def associate_topic_subtopic(topic, subtopic):
    "TODO"

################# TEST - MOVE ONTO SEPARATE FILE ################

def test_make_topic_model():
    topic_fixture = {'base_path': '/topic/working-sea', 'web_url': 'https://www.gov.uk/topic/working-sea', 'content_id': '077826e8-f094', 'description': 'List of information about Working at sea.', 'title': 'Working at sea', 'api_url': 'https://www.gov.uk/api/content/topic/working-sea'}

    created_topic = make_topic_model(topic_fixture)

    expected_topic = Topic(
        title='Working at sea',
        base_path='/topic/working-sea',
        web_url='https://www.gov.uk/topic/working-sea',
        api_url='https://www.gov.uk/api/content/topic/working-sea',
        description='List of information about Working at sea.'
    )

    assert created_topic.title == expected_topic.title
    assert created_topic.base_path == expected_topic.base_path
    assert created_topic.web_url == expected_topic.web_url
    assert created_topic.api_url == expected_topic.api_url
    assert created_topic.description == expected_topic.description

def test_make_subtopic_model():
    subtopic_fixture = {'content_id': '6382617d-a2c5-4651-b487-5d267dfc6662', 'locale': 'en', 'base_path': '/topic/working-sea/health-safety', 'description': 'List of information about Health and safety.', 'api_url': 'https://www.gov.uk/api/content/topic/working-sea/health-safety', 'title': 'Health and safety', 'web_url': 'https://www.gov.uk/topic/working-sea/health-safety'}

    created_subtopic = make_topic_model(subtopic_fixture)

    expected_subtopic = Subtopic(
        title='Health and safety',
        base_path='/topic/working-sea/health-safety',
        web_url='https://www.gov.uk/topic/working-sea/health-safety',
        api_url='https://www.gov.uk/api/content/topic/working-sea/health-safety',
        description='List of information about Health and safety.'
    )

    assert created_subtopic.title == expected_subtopic.title
    assert created_subtopic.base_path == expected_subtopic.base_path
    assert created_subtopic.web_url == expected_subtopic.web_url
    assert created_subtopic.api_url == expected_subtopic.api_url
    assert created_subtopic.description == expected_subtopic.description
