"""Exchanger server DB models."""
import datetime
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, Date, ForeignKey,
                        DateTime, Float)


# DB Tables:
# users:              All the users of the app.      V
# books:              All books that users added.    V
# matches:            Matches between two users.
# categories:         All possible books categories. V
# users_books:        Books that users has.          V
# books_categories:   Categories of books.           V


class User(Base):
    """Holds user info.

    Latitude and longitude represent the base location of the user.
    The matches will consider user base location.
    """
    __tablename__ = 'users'
    books = relationship("Book", secondary='users_books')

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String(25), nullable=False)
    address = Column(String(25), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    join_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.__class__.__name__}: " \
               f"{(self.id, self.name, self.email)}"


class Category(Base):
    """Holds books that users added."""
    __tablename__ = 'categories'
    books = relationship("Book", secondary='books_categories')

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.id, self.name)}"

class Book(Base):
    """Holds books that users added."""
    __tablename__ = 'books'
    users = relationship("User", secondary='users_books')
    categories = relationship("Category", secondary='books_categories')

    title = Column(String)
    author = Column(String)
    description = Column(String)
    publication_date = Column(Date)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"{self.__class__.__name__}: " \
               f"{(self.id, self.title, self.author)}"

class BookCategory(Base):
    """Relationship model between books and categories."""
    __tablename__ = 'books_categories'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'),
                         primary_key=True)

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.book_id, self.category_id)}"
    

class UserBook(Base):
    """Relationship model between books and users."""
    __tablename__ = 'users_books'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)

    def __repr__(self):
        return f"{self.__class__.__name__}: {(self.book_id, self.user_id)}"
    