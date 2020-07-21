"""Books service app."""
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from .db.tables import Base
from .db.config import transaction, engine
from .schemas import NewBookRequest, DeleteBookRequest, BookResponse

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Initiating DB."""
    Base.metadata.create_all(engine)


@app.post("/new_book", status_code=HTTP_201_CREATED)
def add_new_book(request: NewBookRequest):
    """Adding new book.

    Args:
        request (NewBookRequest): Book details.

    Returns:
        dict. Book id.
    """
    return {"book_id": -1}


@app.delete("/delete_book")
def remove_book(request: DeleteBookRequest):
    """Delete book from db.

    Args:
        request (DeleteBookRequest): Book id.
    """
    pass


@app.get("/book/id/{id}", response_model=BookResponse)
def search_book_by_id(id: int):
    """Searching book by book id.

    Args:
        id (int): Book id.
    """
    pass


@app.get("/books/user_id/{user_id}", response_model=List[BookResponse])
def search_books_by_user_id(user_id: int):
    pass


@app.get("/books/user_id/{user_id}/category/{category_id}",
         response_model=List[BookResponse])
def search_category_books_by_user_id(user_id: int, category_id: int):
    pass


@app.get("/books/name/{name_filter}", response_model=List[BookResponse])
def search_books_by_name(name_filter: str):
    pass
