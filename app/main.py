"""Main API endpoints for book exchanger app."""
import re
import logging
from fastapi import FastAPI
from fastapi import HTTPException
from starlette.status import HTTP_201_CREATED

from app.api_models import NewUser
from app.db.models import Category, Book, User
from app.db.config import recreate_database, transaction


class ExchangerApp(FastAPI):
    """FastAPI app server wrapper.

    Setup the exchanger app database and hold app global data.
    """
    EMAIL_FORMAT = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
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

    def validate_email(self, email):
        """Validate user email."""
        if (re.search(self.EMAIL_FORMAT, email)):
            return True
        return False

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


@app.post("/add_user", status_code=HTTP_201_CREATED)
def add_user(user_data: NewUser):
    """Adding new user to DB.

    Args:
        user_data (NewUser): New user target data.
    """
    new_user = User(admin=False, name=user_data.name,
                    password=user_data.password, email=user_data.email,
                    lat=user_data.lat, lan=user_data.lan,
                    address=user_data.address)

    if app.validate_email(user_data.email) is False:
        raise HTTPException(status_code=400, detail="Email is invalid.")

    with transaction() as session:
        users = session.query(User).filter_by(email=user_data.email).all()

    if users:
        raise HTTPException(status_code=400, detail="Email is already used.")

    app.logger.debug("Adding user: %s", str(new_user))
    with transaction() as session:
        session.add(new_user)
        session.commit()

@app.get("/users")
def get_users(filter: str = ""):
    """Get users from the db with optional filter.

    Args:
        filter (str): Optional filter for the users.

    Notes:
        Filtering the users with naive contains.

    Returns:
        json. Filtered users.
    """
    with transaction() as session:
        if filter is not "":
            users = session.query(User).filter(
                User.name.contains(filter)).all()
        else:
            users = session.query(User).all()

    return {"users": users}

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
