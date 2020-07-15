# TODO: Pass each line in each file in the process and study it!
from typing import List

from fastapi import FastAPI, HTTPException

from api.db.tables import Base
from api.api_models import CategoryResponse
from api.db.config import engine, transaction
from api.db.crud import get_categories_by_name, get_all_categories

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(filter: str, limit: int = 100):
    """Get categories from the DB with optional filter.

    Args:
        filter (str): Categories name filter.
        limit (int): Returned categories amount.

    Notes:
        Filtering the categories with naive contains.
    """
    if limit < 0:
        raise HTTPException(status_code=400, detail="Illegal limit.")

    with transaction() as session:
        if filter is not None:
            categories = get_categories_by_name(session, filter, limit)
        else:
            categories = get_all_categories(session, limit)
        return [CategoryResponse(id=category.id, name=category.name)
                for category in categories]
