"""Testing CRUD calls."""
import logging

from sqlalchemy import create_engine
from contextlib2 import contextmanager
from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql

from old_app.db.crud import (get_all_categories, get_categories_by_name,
                             insert_new_category)
from old_app.db.config import (CATEGORIES_FILE, DB_URL, init_categories,
                               get_categories_dataset)

# Tests logger.
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# Startup test db.
temp_test_db = Postgresql()
engine = create_engine(temp_test_db.url(), echo=True)
MockedSession = sessionmaker(bind=engine)
logger.info("Tests DB was created: %s", temp_test_db.url())


@contextmanager
def mocked_transaction():
    s = MockedSession()

    try:
        yield s

    except Exception:
        s.rollback()
        raise

    finally:
        s.close()


def setup_module():
    """Initiating tests temp db.

    Notes:
        Startup function.
    """
    with mocked_transaction() as session:
        init_categories(session=session, engine=engine)
        logger.info("Tests temp db was initiated")


def teardown_module():
    """Stopping tests temp db.

    Notes:
        Teardown function.
    """
    temp_test_db.stop()
    logger.info("Tests temp db was stopped")


def test_get_all_categories():
    """Test getting all categories functionality."""
    with mocked_transaction() as session:
        categories = get_all_categories(session)
    categories_names = set(element.name for element in categories)
    expected_categories = get_categories_dataset()
    assert categories_names == expected_categories


def test_get_not_exist_category():
    """Test getting not exist category functionality."""
    with mocked_transaction() as session:
        categories = get_categories_by_name(session, "not_exist_category")
    assert categories == []


def test_adding_new_category():
    """Test adding new category functionality."""
    tested_category = "test_category"

    with mocked_transaction() as session:
        insert_new_category(session, tested_category)
        categories = get_categories_by_name(session, filter=tested_category)
        assert [category.name for category in categories] == [tested_category]


def test_get_existing_category():
    """Test getting existing category functionality."""
    tested_category = "test_category"
    tested_filter = "test_"

    with mocked_transaction() as session:
        insert_new_category(session, tested_category)
        categories = get_categories_by_name(session, filter=tested_category)
        assert [category.name for category in categories] == [tested_category]
        # Testing filter
        categories = get_categories_by_name(session, filter=tested_filter)
        assert [category.name for category in categories] == [tested_category]