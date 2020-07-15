"""Categories service models."""
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, String, MetaData, Table)

# TODO: Export to environment variable.
DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

metadata = MetaData()
engine = create_engine(DATABASE_URL, echo=True)

categories = Table(
    'categories',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
)

database = Database(DATABASE_URL)
