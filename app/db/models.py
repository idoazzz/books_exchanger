"""Exchanger server DB models."""
import datetime
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, Date, Boolean, ForeignKey, 
                        DateTime)


# DB Tables:
# users:              All the users of the app.      V
# books:              All books that users added.    V
# cities:             Cities that our app support.   V
# matches:            Matches between two users.
# categories:         All possible books categories.
# users_books:        Books that users has.
# books_categories:   Categories of books.


class User(Base):
    """Holds user info."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    admin = Column(Boolean, default=False)
    name = Column(String(25), nullable=False)
    password = Column(String(25), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    join_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("City")
        
    def __repr__(self):
        data = (self.id, self.name, self.email)
        return f"{self.__class__.__name__}: {data}, Admin: {self.admin}"


class City(Base):
    """Holds exchanger app supported cities."""
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True, nullable=False)

    def __repr__(self):
        data = (self.id, self.name)
        return f"{self.__class__.__name__}: {data}"


class Book(Base):
    """Holds books that users added."""
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    publication_date = Column(Date)
 
    def __repr__(self):
        data = (self.id, self.title, self.author, self.description,
                self.publication_date)
        return f"{self.__class__.__name__}: {data}"