import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_definition import Topic, Subtopic

class TopicImporter:
    def make_topic_model(self, topic_data):
        return Topic(
            title=topic_data["title"],
            base_path=topic_data["base_path"],
            web_url=topic_data["web_url"],
            api_url=topic_data["api_url"],
            description=topic_data["description"]
        )

    def make_subtopic_model(self, subtopic_data):
        return Subtopic(
            title=subtopic_data["title"],
            base_path=subtopic_data["base_path"],
            web_url=subtopic_data["web_url"],
            api_url=subtopic_data["api_url"],
            description=subtopic_data["description"]
        )

    def associate_topic_subtopics(self, topic, subtopics):
        topic.subtopics = subtopics

    # Loop through topics
    # Loops through subtopics
    # Assign them to their parents
    # Save all
    def run(self):
        engine = create_engine('sqlite:///klassify.db', echo=True)

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        API_URL = "https://www.gov.uk/api/content"
        root = requests.get(API_URL + "/topic").json()

        topics_json = root["links"]["children"]
        topics = []

        for topic_json in topics_json:
            topic_base_path = topic_json["base_path"]
            subtopics_json = requests.get(API_URL + topic_base_path).json()
            subtopics_json = subtopics_json["links"]["children"]

            topic = make_topic_model(topic_json)
            print("Created:" + topic_json["base_path"])
            topics.append(topic)

            subtopics = []

            for subtopic_json in subtopics_json:
                subtopics.append(make_subtopic_model(subtopic_json))
                print("Created:" + subtopic_json["base_path"])
                associate_topic_subtopics(topic, subtopics)

        session.add_all(topics)
        session.add_all(subtopics)
        session.commit()
