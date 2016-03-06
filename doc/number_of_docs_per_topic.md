## Number of documents per topic

```python
from src.db_handler import DBHandler
from src.tables import Topic, Document

DBH = DBHandler(echo=False)
topics = DBH.session.query(Topic).all()

count_hash = {}
for topic in topics:

    count = 0

    for subtopic in topic.subtopics:

        count = count + len(subtopic.documents)

    count_hash[count] = topic.title

print(sorted(count_hash.items())[::-1])
```

3501: Business tax
1717: Dealing with HMRC
981: Personal tax
634: Environmental management
533: Schools, colleges and children's services
382: Setting up and running a charity
327: Competition
273: Help for British nationals overseas
271: Further education and skills
266: Intellectual property
230: Defence and armed forces
198: Health protection
182: Medicines, medical devices and blood regulation and safety
180: Keeping farmed animals
161: Legal aid
158: Driving tests and learning to drive
137: Business and enterprise
127: Land registration
117: MOT and vehicle testing
113: Benefits
109: Population screening programmes
104: Driving and motorcycle instructors
103: Commercial fishing and fisheries
100: Oil and gas
96: Transport
92: Local government
84: Producing and distributing food
83: Climate change and energy
77: High Speed 2
76: Government
67: Working at sea
66: Housing
60: Company registration and filing
36: Outdoor access and recreation
30: Community organisations
23: Public safety and emergencies
22: Crime and policing
21: Farming and food grants and payments
13: Coal
9: Work and careers
7: Local communities
6: Animal welfare
5: Guidance for government digital publishing and services
4: Prisons and probation
3: Death and wills
