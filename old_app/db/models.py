"""Exchanger server DB models."""
import datetime

from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, Date, ForeignKey,
                        DateTime, Float, LargeBinary)


class User(Base):
    __tablename__ = 'users'
    books = relationship("Book")
    categories = relationship("Category", secondary='users_categories')

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String(25), nullable=False)
    address = Column(String(25), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    join_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.__class__.__name__}: " \
               f"{(self.id, self.name, self.email)}"


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship("Book", secondary='books_categories')
    users = relationship("User", secondary='users_categories')

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.id, self.name)}"

class Book(Base):
    __tablename__ = 'books'
    user = relationship('User')
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=True)
    description = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    id = Column(Integer, primary_key=True, autoincrement=True)
    categories = relationship("Category", secondary='books_categories')


    def __repr__(self):
        return f"{self.__class__.__name__}: " \
               f"{(self.id, self.name, self.author)}"

class BookCategory(Base):
    __tablename__ = 'books_categories'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'),
                         primary_key=True)

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.book_id, self.category_id)}"
    

class UserCategory(Base):
    __tablename__ = 'users_categories'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.cateogry_id, self.user_id)}"

class ExchangeRequest(Base):
    __tablename__ = 'exchange_requests'
    book_id2 = Column(Integer, ForeignKey('books.id'), nullable=True)
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id1 = Column(Integer, ForeignKey('books.id'), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.request_id)}"