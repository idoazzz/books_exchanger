"""Categories service app."""
from typing import List

from fastapi import FastAPI, HTTPException

from .db.tables import Base
from .schemas import CategoryResponse
from .db.config import engine, transaction, import_categories
from .db.crud import get_categories_by_name, get_all_categories

Base.metadata.create_all(engine)
import_categories()

app = FastAPI()


@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(filter: str = None):
    """Get categories from the DB with optional filter.

    Args:
        filter (str): Categories name filter.

    Notes:
        Filtering the categories with naive contains.
    """
    with transaction() as session:
        if filter is not None:
            categories = get_categories_by_name(session, filter)
        else:
            categories = get_all_categories(session)
        return [CategoryResponse(id=category.id, name=category.name)
                for category in categories]
