"""Categories service old_app."""
from typing import List

from fastapi import FastAPI, Depends

from .schemas import CategoryResponse
from .db.crud import get_categories_by_name, get_all_categories
from .db.config import transaction, init_categories, Session, engine

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
