from starlette.testclient import TestClient

from app.main import app
from app.db.config import CATEGORIES_FILE

client = TestClient(app)


def test_get_all_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    with open(CATEGORIES_FILE) as file:
        assert response.json() == file.readlines()
