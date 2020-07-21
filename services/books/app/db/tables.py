"""Books service db models."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, ARRAY, LargeBinary, Date)

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    categories_ids = Column(ARRAY(Integer))
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    image = Column(LargeBinary, nullable=True)
    description = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Book ({self.id}), User {self.user_id}: {self.name}"