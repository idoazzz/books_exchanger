"""DB configurations and utils."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .tables import Base
from .crud import insert_new_category, get_all_categories

CATEGORIES_FILE = "app/db/categories.txt"

# NOTE: Env.py has duplication.
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


def get_categories_dataset():
    """Read categories from dataset file."""
    with open(CATEGORIES_FILE, mode="r") as file:
        return set(element.strip() for element in file.readlines())


def init_categories(engine, session):
    """Inserting categories data set if it's not exist."""
    Base.metadata.create_all(engine)
    if len(get_all_categories(session)) == 0:
        for category in get_categories_dataset():
            insert_new_category(session, name=category.strip())
        session.commit()
