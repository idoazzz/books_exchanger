"""Main API endpoints for book exchanger app."""
import logging
from fastapi import FastAPI

from app.db.routers import books
from app.db.routers import users
from app.db.models import Category
from app.db.routers import categories
from app.db.config import recreate_database, transaction


class ExchangerApp(FastAPI):
    """FastAPI app server wrapper.

    Setup the exchanger app database and hold app global data.
    """
    CATEGORIES_FILE = "categories.txt"

    def __init__(self, rebuild_db=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.DEBUG)
        self.setup_exchanger_server(rebuild_db)

    def setup_exchanger_server(self, rebuild_db):
        """Initialize exchanger app server.

        Args:
            rebuild_db (bool): Building new empty db.
        """
        if rebuild_db:
            self.logger.debug("Creating the database")
            recreate_database()
            self.import_categories()

    def import_categories(self):
        """Import predefined categories from a file to DB."""
        with open(self.CATEGORIES_FILE) as file, transaction() as session:
            categories = set(file.readlines())
            self.logger.debug("Adding categories: %s", str(categories))
            for category in categories:
                session.add(Category(name=category.strip()))
            session.commit()

app = ExchangerApp()
app.include_router(users.router)
app.include_router(books.router)
app.include_router(categories.router)


# TODO: Adding cities to the DB - (?)
# TODO: Adding book endpoint.
# TODO: Get books with filter endpoint.
# TODO: Adding new category endpoint.
# TODO: Delete book endpoint.
# TODO: Deleting user endpoint.
# TODO: Get all books by category and radius near lat lan.
# TODO: Get specific user matches (Build model in DB).
# TODO: Get specific user books.
# TODO: Authentication to each endpoint.
