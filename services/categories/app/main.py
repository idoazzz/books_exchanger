"""Categories service app."""
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .schemas import CategoryResponse
from .db.config import transaction, init_categories, Session, engine
from .db.crud import (get_categories_by_name, get_all_categories,
                      get_category_by_id)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Initiating DB."""
    session = Session()
    init_categories(session=session, engine=engine)
    session.close()


@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(filter: str = None, session=Depends(transaction)):
    """Get categories from the DB with optional filter.

    Args:
        session (Session): DB session.
        filter (str): Categories name filter.

    Notes:
        Filtering the categories with naive contains.
    """
    if filter is not None:
        categories = get_categories_by_name(session, filter)
    else:
        categories = get_all_categories(session)
    return [CategoryResponse(id=category.id, name=category.name)
            for category in categories]


@app.get("/category/{id}", response_model=CategoryResponse)
def get_categories_by_user_id(id: int, session=Depends(transaction)):
    """Get categories from the DB with optional filter.

    Args:
        id (int): Category id.
        session (Session): DB session.
    """
    category = get_category_by_id(session, id)
    if category is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Category was not found.")
    return CategoryResponse(id=category.id, name=category.name)
