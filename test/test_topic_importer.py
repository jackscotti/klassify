from klassify.src.topic_importer import TopicImporter
from klassify.src.table_definition import Topic, Subtopic

def importer():
    return TopicImporter()

def test_make_topic_model():
    topic_fixture = {'base_path': '/topic/working-sea', 'web_url': 'https://www.gov.uk/topic/working-sea', 'content_id': '077826e8-f094', 'description': 'List of information about Working at sea.', 'title': 'Working at sea', 'api_url': 'https://www.gov.uk/api/content/topic/working-sea'}

    created_topic = importer().make_topic_model(topic_fixture)

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

    created_subtopic = importer().make_topic_model(subtopic_fixture)

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

def test_associate_topic_subtopics():
    topic = Topic(title="A topi title")
    subtopic_1 = Subtopic(title="A subtopic title 1")
    subtopic_2 = Subtopic(title="A subtopic title 2")

    importer().associate_topic_subtopics(topic, [subtopic_1, subtopic_2])

    assert subtopic_1.title == topic.subtopics[0].title
    assert subtopic_2.title == topic.subtopics[1].title
