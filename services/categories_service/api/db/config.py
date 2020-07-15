from sqlalchemy import create_engine
from contextlib2 import contextmanager
from sqlalchemy.orm import sessionmaker

from api.db.crud import insert_new_category, get_all_categories

CATEGORIES_FILE = "api/db/categories.txt"

# TODO: Export to environment variable.
DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def transaction():
    s = Session()
    try:
        yield s

    except:
        s.rollback()
        raise

    finally:
        s.close()

# Inserting categories data set.
with transaction() as session:
    if len(get_all_categories(session)) == 0:
        with open(CATEGORIES_FILE) as file:
            for category in set(file.readlines()):
                insert_new_category(session, name=category)
            session.commit()