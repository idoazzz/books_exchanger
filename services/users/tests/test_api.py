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
                 password, password2):
        super(NewMockedUser, self).__init__(id, name, email, address, latitude,
                                            longitude)
        self.password = password
        self.password2 = password2


# Test /add_user endpoint.

def send_add_user_request(mocker, id, name, email, address, latitude,
                          longitude, password, password2, user_exists=False):
    """Create mocked user and send add_user request.

    Returns:
        response (Response). HTTP response.
    """
    mocked_user = NewMockedUser(id, name, email, address, latitude,
                                longitude, password, password2)
    mocker.patch('app.main.get_user_by_email', return_value=user_exists)
    mocker.patch('app.main.add_user', return_value=mocked_user)
    return client.post(f"/add_user", json=mocked_user.__dict__)


def test_add_valid_user(mocker):
    """Test adding valid user."""
    password = fake.password()
    response = send_add_user_request(mocker, 1, fake.name(), fake.email(),
                                     fake.address(), float(fake.latitude()),
                                     float(fake.longitude()), password,
                                     password)
    assert response.status_code == 201
    assert response.json()["user_id"] == 1


def test_add_already_exist_user(mocker):
    """Test adding valid user."""
    password = fake.password()
    response = send_add_user_request(mocker, 1, fake.name(), fake.email(),
                                     fake.address(), float(fake.latitude()),
                                     float(fake.longitude()), password,
                                     password, user_exists=True)
    assert response.status_code == 400


def test_add_invalid_user(mocker):
    """Test adding invalid user (email and password)."""
    # Invalid password.
    invalid_emails = ["INVALID_EMAIL", "12311", "idoa@.com", "i@."]
    password = "FAKE_PASSWORD"
    password2 = "FAKE_PASSWORD_2"

    for email in invalid_emails:
        response = send_add_user_request(mocker, 1, fake.name(), email,
                                         fake.address(),
                                         float(fake.latitude()),
                                         float(fake.longitude()), password,
                                         password)
        assert response.status_code == 400

    # Check not matching password.
    response = send_add_user_request(mocker, 1, fake.name(), email,
                                     fake.address(), float(fake.latitude()),
                                     float(fake.longitude()), password,
                                     password2)
    assert response.status_code == 400


# Test /delete_user endpoint.

def test_delete_exists_user(mocker):
    """Test delete exists user functionality."""
    user_exists = True
    email = fake.email()
    password = fake.password()
    mocker.patch('app.main.delete_user', return_value=user_exists)
    delete_request = {'email': email, 'password': password}
    response = client.delete(f"/delete_user", json=delete_request)
    assert response.status_code == 200


def test_delete_not_exists_user(mocker):
    """Test delete not exists user functionality."""
    user_exists = False
    email = fake.email()
    password = fake.password()
    mocker.patch('app.main.delete_user', return_value=user_exists)
    delete_request = {'email': email, 'password': password}
    response = client.delete(f"/delete_user", json=delete_request)
    assert response.status_code == 400


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


# Test /geosearch endpoint.

def test_get_exists_users_by_location(mocker):
    """Test get exists user by id functionality."""
    mocked_users = [MockedUser(id, fake.name(), fake.email(),
                              fake.address(), float(fake.latitude()),
                              float(fake.longitude())) for id in range(10)]
    mocker.patch('app.main.get_near_users', return_value=mocked_users)
    response = client.get(f"/geosearch", longitude=fake.longitude(),
                          latitude=fake.latitude(), radius=50)
    assert response.status_code == 200
    import ipdb; ipdb.set_trace()