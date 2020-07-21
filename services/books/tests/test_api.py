"""Testing API calls."""
from faker import Faker
from starlette.testclient import TestClient

from app.main import app

fake = Faker()
client = TestClient(app)