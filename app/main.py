"""Main API endpoints for book exchanger app."""
import logging
from fastapi import FastAPI

from app.db.config import recreate_database, transaction
from app.db.models import Category

class ExchangerApp(FastAPI):
    """FastAPI app server wrapper.

    Setup the exchanger app database and hold the global data.
    """
    CATEGORIES_FILE = "categories.txt"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.DEBUG)
        self.setup_exchanger_server()

    def setup_exchanger_server(self):
        """Initialize exchanger app server."""
        self.logger.debug("Creating the database")
        recreate_database()
        self.logger.debug("Initialize categories table")
        self.import_categories()

    def import_categories(self):
        """Import predefined categories from a file to DB."""
        with open(self.CATEGORIES_FILE) as file, transaction() as session:
            categories = set(file.readlines())
            for category in categories:
                session.add(Category(name=category.strip()))
            self.logger.debug("Adding categories: %s", str(categories))
            session.commit()


app = ExchangerApp()

@app.get("/categories")
def get_categories(filter: str = ""):
    """Get categories from the db with optional filter.

    Args:
        filter (str): Optional filter for the categories.

    Notes:
        Filtering the categories with naive contains.

    Returns:
        json. Filtered categories.
    """
    with transaction() as session:
        if filter is not "":
            categories = session.query(Category).filter(
                Category.name.contains(filter)).all()
        else:
            categories = session.query(Category).all()

    categories_names = list(map(lambda element: str(element.name), categories))
    return {"categories": categories_names}

# TODO: Adding cities to the DB.
# TODO: Adding book endpoint.
# TODO: Get books with filter endpoint.
# TODO: Adding new category endpoint.
# TODO: Delete book endpoint.
# TODO: Adding user endpoint (Register).
# TODO: Deleting user endpoint.
# TODO: Get all books by category and radius near lat lan.
# TODO: Get specific user matches (Build model in DB).
# TODO: Get specific user books.
# TODO: Authentication to each endpoint.
