import logging
from fastapi import FastAPI

from app.db.config import recreate_database, transaction
from app.db.models import Category

app = FastAPI()
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

logger.debug("Creating the database...")
recreate_database()

logger.debug("Initialize categories table...")
with open("categories.txt") as file, transaction() as session:
    categories = set(file.readlines())
    for category in categories:
        logger.debug("Adding category: %s", category)
        session.add(Category(name=category.strip()))
        session.commit()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/categories")
def get_categories():
    """Get categories from the db and return JSON result."""
    with transaction() as session:
        categories = session.query(Category).all()

    categories_names = \
        list(map(lambda category: str(category.name), categories))
    return {"categories": categories_names}