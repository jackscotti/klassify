from src.topic_importer import TopicImporter
from src.document_importer import DocumentImporter
from src.content_importer import ContentImporter
import os
#
# database_name = "klassify"
#
# if os.path.exists("%s.db" % database_name):
#     os.remove("%s.db" % database_name)
#
# # Add topics and subtopics
# TopicImporter().run()
# # Add documents and associate them subtopics
# DocumentImporter().run()
ContentImporter().import_documents_html()
# import pdb; pdb.set_trace()
