# Appendix C2 - topic_importer.py

import requests
from .tables import Topic, Subtopic
from .db_handler import DBHandler

class TopicImporter:
    def __init__(self):
        self.session = DBHandler(echo=False).session
        self.API_URL = "https://www.gov.uk/api/content"

    def make_topic(self, topic_data):
        return Topic(title=topic_data["title"],
            base_path=topic_data["base_path"], web_url=topic_data["web_url"],
            api_url=topic_data["api_url"], description=topic_data["description"])
    def make_subtopic(self, subtopic_data):
        return Subtopic(title=subtopic_data["title"],
            base_path=subtopic_data["base_path"], web_url=subtopic_data["web_url"],
            api_url=subtopic_data["api_url"], description=subtopic_data["description"])

    def associate_topic_subtopics(self, topic, subtopics):
        topic.subtopics = subtopics

    def run(self):
        root = requests.get(self.API_URL + "/topic").json()
        topics_json = root["links"]["children"]

        topics = []
        print("Importing topics and subtopics", end="", flush=True)
        for topic_json in topics_json:
            print('.', end="", flush=True)
            topic = self.make_topic(topic_json)
            topics.append(topic)

            topic_base_path = topic_json["base_path"]
            topic_data = requests.get(self.API_URL + topic_base_path).json()
            subtopics_json = topic_data["links"]["children"]
            subtopics = []
            for subtopic_json in subtopics_json:
                subtopics.append(self.make_subtopic(subtopic_json))
                self.associate_topic_subtopics(topic, subtopics)

        self.session.add_all(topics)
        self.session.add_all(subtopics)
        self.session.commit()
        print("\nComplete.")
