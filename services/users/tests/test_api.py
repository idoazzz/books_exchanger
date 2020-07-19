"""Testing API calls."""
import logging

from faker import Faker
from starlette.testclient import TestClient

from app.main import app

fake = Faker()
client = TestClient(app)


class MockedUser:
    """Mocked user object."""

    def __init__(self, id, name, email, address, latitude, longitude):
        self.id = id
        self.name = name
        self.email = email
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


class NewMockedUser(MockedUser):
    def __init__(self, id, name, email, address, latitude, longitude,
                 password):
        super(NewMockedUser, self).__init__(id, name, email, address, latitude,
                                            longitude)
        self.password = password


# Test /add_user endpoint.

def test_add_valid_user(mocker):
    """Test get not-exists user by id functionality."""
    mocked_user = NewMockedUser(1, fake.name(), fake.email(),
                             fake.address(), float(fake.latitude()),
                             float(fake.longitude()), fake.password())
    mocker.patch('app.main.get_user_by_email', return_value=None)
    mocker.patch('app.main.add_user', return_value=mocked_user)
    response = client.post(f"/add_user", json=mocked_user.__dict__)
    assert response.status_code == 201
    assert response.json()["user_id"] == 1


# Test /user/ endpoint.

def test_get_exists_user_by_id(mocker):
    """Test get exists user by id functionality."""
    fake_user_id = 1012
    mocked_user = MockedUser(fake_user_id, fake.name(), fake.email(),
                             fake.address(), float(fake.latitude()),
                             float(fake.longitude()))
    mocker.patch('app.main.get_user_by_id', return_value=mocked_user)
    response = client.get(f"/users/id/{fake_user_id}")
    assert response.status_code == 200
    assert mocked_user.__dict__ == response.json()


def test_get_not_exists_user_by_id(mocker):
    """Test get not-exists user by id functionality."""
    fake_user_id = 1012
    mocker.patch('app.main.get_user_by_id', return_value=None)
    response = client.get(f"/users/id/{fake_user_id}")
    assert response.status_code == 400


def test_get_type_user_by_invalid_id():
    """Test get user with illegal id functionality."""
    fake_user_id = "STRING"
    response = client.get(f"/users/id/{fake_user_id}")
    assert response.status_code == 400


def test_get_exists_user_by_email(mocker):
    """Test get exists user by id functionality."""
    fake_user_email = "abc@gmail.com"
    mocked_user = MockedUser(1, fake.name(), fake_user_email,
                             fake.address(), float(fake.latitude()),
                             float(fake.longitude()))
    mocker.patch('app.main.get_user_by_email', return_value=mocked_user)
    response = client.get(f"/users/email/{fake_user_email}")
    assert response.status_code == 200
    assert mocked_user.__dict__ == response.json()


def test_get_not_exists_user_by_email(mocker):
    """Test get not-exists user by id functionality."""
    mocker.patch('app.main.get_user_by_email', return_value=None)
    response = client.get(f"/users/email/{fake.email()}")
    assert response.status_code == 400


def test_get_type_user_by_invalid_email():
    """Test get user with illegal id functionality."""
    fake_user_emails = ["NOT_VALID_EMAIL", "ido@gmail.com!", "if...."]
    for email in fake_user_emails:
        response = client.get(f"/users/email/{email}")
        assert response.status_code == 400


# Test /authenticate_user endpoint.

def test_exists_user_authentication(mocker):
    """Test get not-exists user by id functionality."""
    mocker.patch('app.main.is_authenticated_user', return_value=True)
    fake_user = {'email': fake.email(), 'password': fake.password()}
    response = client.post(f"/authenticate_user", json=fake_user)
    assert response.status_code == 200


def test_not_exists_user_authentication(mocker):
    """Test get not-exists user by id functionality."""
    mocker.patch('app.main.is_authenticated_user', return_value=False)
    response = client.get(f"/users/email/{fake.email()}")
    assert response.status_code == 400


def test_authentication_with_invalid_email():
    """Test get user with illegal id functionality."""
    fake_user_emails = ["NOT_VALID_EMAIL", "ido@gmail.com!", "if...."]
    for email in fake_user_emails:
        response = client.get(f"/users/email/{email}")
        assert response.status_code == 400
