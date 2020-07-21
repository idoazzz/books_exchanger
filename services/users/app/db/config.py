"""DB configurations and utils."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# NOTE: Env.py has duplication.
DB_NAME = os.environ.get("DB_NAME", "users")
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
