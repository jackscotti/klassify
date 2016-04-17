# Appendix C1 - setup.py

# Install nltk modules
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from src.topic_importer import TopicImporter
from src.document_importer import DocumentImporter
from src.content_importer import ContentImporter
import os

database_name = "klassify"
if os.path.exists("%s.db" % database_name):
    os.remove("%s.db" % database_name)

# Add topics and subtopics
print("Importing topics and subtopics:")
TopicImporter().run()

# Add documents and associate them subtopics
print("Importing documents:")
DocumentImporter().run()

print("Importing documents HTML:")
ContentImporter().import_documents_html()

print("Importing documents data:")
ContentImporter().extract_documents_content()
