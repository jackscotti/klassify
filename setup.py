from src.topic_importer import TopicImporter
from src.document_importer import DocumentImporter

# Add topics and subtopics
TopicImporter().run()
# Add documents and associate them subtopics
DocumentImporter().run()
