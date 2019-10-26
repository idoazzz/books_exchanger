"""Contains DB configurations."""
import os
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


PORT = os.environ.get('POSTGRES_PORT', '5432')
DB = os.environ.get('POSTGRES_DB', 'exchanger')
HOST = os.environ.get('POSTGRES_HOST', 'db')
USERNAME = os.environ.get('POSTGRES_USERNAME', 'exchanger')
PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'exchanger')
DATABASE_URI = f'postgres+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

engine = create_engine(DATABASE_URI)
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


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # Can create here test environment for DB.
