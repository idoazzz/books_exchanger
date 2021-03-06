"""Categories service db models."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    name = Column(String, unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Category {self.id}: {self.name}"
