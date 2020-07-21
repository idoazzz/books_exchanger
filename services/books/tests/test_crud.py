"""Testing CRUD calls."""
import logging

from faker import Faker

from app.db.tables import Base
from sqlalchemy import create_engine
from contextlib2 import contextmanager
from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql

# Tests logger.
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# Startup test db.
fake = Faker()
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


def setup_function():
    """Initiating tests temp db in each test.

    Notes:
        Startup function.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Tests temp db was initiated")


def teardown_module():
    """Stopping tests temp db.

    Notes:
        Teardown function.
    """
    temp_test_db.stop()
    logger.info("Tests temp db was stopped and deleted")
