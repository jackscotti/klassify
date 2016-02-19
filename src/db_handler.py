from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from klassify.src.base import Base

class DBHandler(object):
    def __init__(self, db_name="klassify"):
        self.db = "sqlite:///%s.db" % db_name
        self.engine = create_engine(self.db, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def destroy_db(self):
        return "TODO"
