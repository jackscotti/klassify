# klassify

An intelligent system with the aim to classify documents.

## Training data / Labeled data:

GOV.UK documents (pages) that are tagged to a topic.

List of urls of documents tagged to a topic and the topics they're tagged to:

https://www.gov.uk/api/search.json?reject_specialist_sectors=_MISSING

## Non labeled data:

List of urls of documents non tagged to a topic:

https://www.gov.uk/api/search.json?filter_specialist_sectors=_MISSING

## Labels:

Topics and subtopics. Available at:

https://www.gov.uk/topic


# Data structure

## Database Entities

Topic
- title       = Column(String)
- base_path   = Column(String)
- description = Column(String)
- Subtopics

Subtopic
- title       = Column(String)
- base_path   = Column(String)
- description = Column(String)
- Topic
- Documents

Document
- title     = Column(String)
- base_path = Column(String)
- html      = Column(Text)
- Subtopics

## Relationships

Topic has many Subtopics
Subtopic has many Documents
Document has many Subtopics

# Testing

From the root directoy, run:

`py.test`

# Setup:

From the root directoy, run:

`python3 setup.py`

The script will build the database, navigate GOV.UK's API and import the data into it.

# Requirements:

- Python 3
- **TODO**: list all the libraries necessary to run the system
