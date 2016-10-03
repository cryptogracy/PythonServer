
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(Engine)


def create_schema():
    Base.metadata.create_all(Engine)

