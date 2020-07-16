"""Testing API calls."""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql
from starlette.testclient import TestClient

from app.main import app
from app.db.config import CATEGORIES_FILE, DB_URL, transaction, init_categories


# TODO: MAKE IT CLASS AND MAKE CRUD TESTING!
# TODO: THINK ABOUT TESTING THE API ONLY WITH MOCKED DICS INSTEAD OF DB!
# TODO: ASK ELRAN ABOUT THE TESTS!
# TODO: ALEMBIC SUPPORT!

class TestAPIEndpoints:
    def __init__(self):
        pass

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass


# Tests logger.
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# Startup test db.
temp_test_db = Postgresql()
engine = create_engine(temp_test_db.url(), echo=True)
MockedSession = sessionmaker(bind=engine)
logger.info("Tests DB was created: %s", temp_test_db.url())

client = TestClient(app)


def mocked_transaction():
    s = MockedSession()

    try:
        yield s

    except Exception:
        s.rollback()
        raise

    finally:
        s.close()


app.dependency_overrides[transaction] = mocked_transaction


def setup_module():
    """Initiating tests temp db.

    Notes:
        Startup function.
    """
    session = MockedSession()
    init_categories(session=session, engine=engine)
    session.close()
    logger.info("Tests temp db was initiated")


def teardown_module():
    """Stopping tests temp db.

    Notes:
        Teardown function.
    """
    temp_test_db.stop()
    logger.info("Tests temp db was stopped")


def test_get_all_categories():
    """Test get all categories functionality."""
    response = client.get("/categories")
    assert response.status_code == 200

    categories_response = set(element["name"] for element in response.json())
    with open(CATEGORIES_FILE, mode="r") as file:
        expected_categories = \
            set(element.strip() for element in file.readlines())
    assert categories_response == expected_categories


def test_get_not_exist_category():
    """Test get not exist category functionality."""
    response = client.get("/categories?filter=not_exist")
    assert response.status_code == 200
    assert response.json() == []
