# TODO: Pass each line in each file in the process and study it!
from typing import List
from fastapi import FastAPI

from api.db_models import metadata, database, engine
from api.api_models import CategoryRequest, CategoryResponse

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/categories", response_model=List[CategoryResponse])
async def get_categories(query: CategoryIn):
    """Get categories from the DB with optional filter.

    Args:
        filter (str): Categories name filter.

    Notes:
        Filtering the categories with naive contains.
    """
    if filter is not None:
        return await get_categories_by_name(query.filter, query.limit)
    return await get_all_categories(query.limit)