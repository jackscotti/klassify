from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from klassify.src.base import Base
import os

class DBHandler(object):
    def __init__(self, db_name="klassify"):
        self.db_name = db_name
        self.db = "sqlite:///%s.db" % self.db_name
        self.engine = create_engine(self.db, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def destroy_db_if_present(self):
        if os.path.exists("%s.db" % self.db_name):
            print("Removing %s database" % self.db_name)
            os.remove("%s.db" % self.db_name)
