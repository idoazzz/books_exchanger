"""Testing API calls."""
import logging

from starlette.testclient import TestClient

from app.main import app

# Tests logger.
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

client = TestClient(app)


class MockedCategory:
    """Mocked category object."""
    def __init__(self, id, name):
        self.id = id
        self.name = name


def test_get_all_categories(mocker):
    """Test get all categories functionality."""
    mocked_categories = [MockedCategory(1, "test1"),
                         MockedCategory(1, "test2")]
    mocker.patch('app.main.get_all_categories', return_value=mocked_categories)
    response = client.get("/categories")
    assert response.status_code == 200
    categories_response = set(element["name"] for element in response.json())
    expected_categories = set(element.name for element in mocked_categories)
    assert categories_response == expected_categories


def test_get_not_exist_category(mocker):
    """Test get not exist category functionality."""
    not_existing_category = "not_exist"
    mocker.patch('app.main.get_categories_by_name', return_value=[])
    response = client.get(f"/categories?filter={not_existing_category}")
    assert response.status_code == 200
    assert response.json() == []
