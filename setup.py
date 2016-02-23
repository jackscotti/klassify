from src.topic_importer import TopicImporter
from src.document_importer import DocumentImporter
import os

database_name = "klassify"

if os.path.exists("%s.db" % database_name):
    os.remove("%s.db" % database_name)

# Add topics and subtopics
TopicImporter().run()
# Add documents and associate them subtopics
DocumentImporter().run()
