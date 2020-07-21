"""Testing API calls."""
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


class MockedCategory:
    """Mocked category object."""

    def __init__(self, id, name):
        self.id = id
        self.name = name


def test_get_all_categories(mocker):
    """Test get all categories functionality."""
    mocked_categories = [MockedCategory(1, "test1"),
                         MockedCategory(2, "test2")]
    mocker.patch('app.main.get_all_categories', return_value=mocked_categories)
    response = client.get("/categories")
    assert response.status_code == 200
    categories_response = set(element["name"] for element in response.json())
    expected_categories = set(element.name for element in mocked_categories)
    assert categories_response == expected_categories


def test_get_not_exists_category_by_name(mocker):
    """Test get not exists category (name search) functionality."""
    not_existing_category = "not_exist"
    mocker.patch('app.main.get_categories_by_name', return_value=[])
    response = client.get(f"/categories?filter={not_existing_category}")
    assert response.status_code == 200
    assert response.json() == []


def test_get_not_exists_category_by_id(mocker):
    """Test get not exists category (id search) functionality."""
    mocker.patch('app.main.get_category_by_id', return_value=None)
    response = client.get("/category/1")
    assert response.status_code == 400


def test_get_exists_category_by_id(mocker):
    """Test ge exists category (id search) functionality."""
    mocked_category = MockedCategory(1, "test1")
    mocker.patch('app.main.get_category_by_id', return_value=mocked_category)
    response = client.get("/category/1")
    assert response.status_code == 200
    assert response.json() == mocked_category.__dict__
