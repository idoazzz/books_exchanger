import logging
from fastapi import FastAPI

from app.db.config import recreate_database, transaction
from app.db.models import Category

app = FastAPI()
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

logger.debug("Creating the database...")
recreate_database()

logger.debug("Init categories table...")
with open("categories.txt") as file, transaction() as session:
    categories = set(file.readlines())
    for category in categories:
        logger.debug("Adding category: %s", category)
        session.add(Category(name=category))
        session.commit()

    session.query(Category).all()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
