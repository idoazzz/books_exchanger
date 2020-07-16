"""Testing API calls."""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql
from starlette.testclient import TestClient

from app.main import app
from app.db.config import CATEGORIES_FILE, DB_URL, transaction, init_categories

# Tests logger.
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# Startup test db.
temp_test_db = Postgresql()
logger.info("Creating tests db: %s", temp_test_db.url())
engine = create_engine(temp_test_db.url(), echo=True)
MockedSession = sessionmaker(bind=engine)

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
    """Initiating tests temp db."""
    session = MockedSession()
    logger.info("Initiating tests temp db")
    init_categories(session=session, engine=engine)
    session.close()


def teardown_module(module):
    """Stopping tests temp db."""
    logger.info("Stopping tests temp db")
    temp_test_db.stop()


def test_get_all_categories(monkeypatch):
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
