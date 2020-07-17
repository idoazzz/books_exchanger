"""Users service db models."""
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, Float, DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    categories_ids = Column(ARRAY(Integer))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String(25), nullable=False)
    address = Column(String(25), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    join_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"User {self.id}: [{(self.name, self.email)}"