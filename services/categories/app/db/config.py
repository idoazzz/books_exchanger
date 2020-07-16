"""DB configurations and utils."""
import os

from sqlalchemy import create_engine
from contextlib2 import contextmanager
from sqlalchemy.orm import sessionmaker

from .tables import Base
from .crud import insert_new_category, get_all_categories

CATEGORIES_FILE = "app/db/categories.txt"

DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_USERNAME = os.environ.get("DB_USERNAME", "postgres")
DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)


def transaction():
    s = Session()
    try:
        yield s

    except Exception:
        s.rollback()
        raise

    finally:
        s.close()


def init_categories(engine, session):
    """Inserting categories data set if it's not exist."""
    Base.metadata.create_all(engine)
    if len(get_all_categories(session)) == 0:
        with open(CATEGORIES_FILE) as file:
            for category in set(file.readlines()):
                insert_new_category(session, name=category.strip())
            session.commit()