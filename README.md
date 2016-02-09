# klassify

# Data structure

## Entities

Topic

- title       = Column(String)
- base_path   = Column(String)
- description = Column(String)
- web_url     = Column(String)
- api_url     = Column(String)
- Subtopics

Subtopic

- title       = Column(String)
- base_path   = Column(String)
- description = Column(String)
- web_url     = Column(String)
- api_url     = Column(String)
- Topic
- Documents

Document

- title     = Column(String)
- base_path = Column(String)
- web_url   = Column(String)
- api_url   = Column(String)
- html      = Column(Text)

## Relationships

Topic has many Subtopics
Subtopic has many Documents
Document has many Subtopics
