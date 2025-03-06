from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    currency = Column(String(10), nullable=False)
    date_ = Column(TIMESTAMP, nullable=False)
    price = Column(DECIMAL(20, 8), nullable=False) 