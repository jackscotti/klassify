from src.topic_importer import TopicImporter
from src.doc_finder import DocFinder

# Add topics and subtopics
TopicImporter().run()
# Add documents and associate them subtopics
DocFinder().run()
