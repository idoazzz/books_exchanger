"""Books API endpoints models."""
from datetime import date

from pydantic import BaseModel


class NewBookRequest(BaseModel):
    name: str
    author: str
    user_id = int
    description: str
    categories_ids: list
    publication_date: date


class DeleteBookRequest(BaseModel):
    book_id: int


class BookResponse(BaseModel):
    id: int
    name: str
    author: str
    user_id = int
    description: str
    categories_ids: list
    publication_date: date

