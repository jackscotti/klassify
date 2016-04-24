# Implementation of a Multi-Label Intelligent Agent: Classifying GOV.UK Content

By Jacopo Scotti.

BSc Information Systems and Management Project Report,
Birkbeck College, University of London, 2016.

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

![Data Model](/doc/img/data-model.png "Data Model")

# Project setup:

## Principal requirements:

- [Python](https://www.python.org/downloads/) - Version > 3.3
- [pip](https://pypi.python.org/pypi/pip)

## Download and install required packages:

From the root directory, run:

`pip3 install -r requirements.txt`

## Import data:

From the root directory, run:

`python3 setup.py`

The script will build the database, navigate GOV.UK's API and import the data into it.

# Testing

From the root directory, run:

`py.test`
