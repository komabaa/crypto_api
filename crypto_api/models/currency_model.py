from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    currency = Column(String, nullable=False)
    date_ = Column(DateTime, default=datetime.datetime.utcnow)
    price = Column(Float, nullable=False)

def get_engine(database_url):
    return create_engine(database_url)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session() 