"""Testing CRUD calls."""
import logging

from faker import Faker

from app.db.tables import Base
from sqlalchemy import create_engine
from contextlib2 import contextmanager
from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql
from app.db.crud import (get_near_users, add_user, get_all_users, delete_user,
                         get_user_by_id, is_authenticated_user,
                         get_user_by_email, update_categories_to_user)

# Tests logger.
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# Startup test db.
fake = Faker()
temp_test_db = Postgresql()
engine = create_engine(temp_test_db.url(), echo=True)
MockedSession = sessionmaker(bind=engine)
logger.info("Tests DB was created: %s", temp_test_db.url())


@contextmanager
def mocked_transaction():
    s = MockedSession()

    try:
        yield s

    except Exception:
        s.rollback()
        raise

    finally:
        s.close()


def setup_function():
    """Initiating tests temp db in each test.

    Notes:
        Startup function.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Tests temp db was initiated")


def teardown_module():
    """Stopping tests temp db.

    Notes:
        Teardown function.
    """
    temp_test_db.stop()
    logger.info("Tests temp db was stopped and deleted")


def test_delete_exists_user():
    """Test deleting user."""
    with mocked_transaction() as session:
        not_hashed_password = fake.password()
        user = add_user(session, fake.name(), fake.email(),
                        not_hashed_password, fake.address(), fake.latitude(),
                        fake.longitude())
        assert user is not None
        assert delete_user(session, user.email, not_hashed_password) == True
        assert get_user_by_id(session, user.id) is None


def test_delete_not_exists_user():
    """Test deleting user."""
    with mocked_transaction() as session:
        not_hashed_password = "password"
        not_existing_user = "not_existing_user"
        assert is_authenticated_user(session, not_existing_user,
                                     not_hashed_password) == False
        assert delete_user(session, not_existing_user,
                           not_hashed_password) == False


def test_add_new_user():
    """Test adding new user."""
    with mocked_transaction() as session:
        user = add_user(session, fake.name(), fake.email(), fake.password(),
                        fake.address(), fake.latitude(), fake.longitude())
        assert user is not None
        assert get_user_by_id(session, user.id) is not None


def test_authenticate_user():
    """Test user authentication."""
    with mocked_transaction() as session:
        not_hashed_password = fake.password()
        user = add_user(session, fake.name(), fake.email(),
                        not_hashed_password, fake.address(), fake.latitude(),
                        fake.longitude())
        assert user is not None
        assert is_authenticated_user(session, user.email, not_hashed_password) \
               is True


def test_authenticate_invalid_user():
    """Test invalid user authentication."""
    password = "password"
    not_existing_user = "not_existing_user"
    with mocked_transaction() as session:
        assert is_authenticated_user(session, not_existing_user, password) \
               is False


def test_get_exist_user_by_email():
    """Test search exists user by email."""
    email = fake.email()
    with mocked_transaction() as session:
        assert get_user_by_email(session, email) is None
        user = add_user(session, fake.name(), email, fake.password(),
                        fake.address(), fake.latitude(), fake.longitude())
        assert user is not None
        assert get_user_by_email(session, user.email) is not None


def test_get_not_exist_user_by_email():
    """Test search not exists user by email."""
    email = "not_existing_email"
    with mocked_transaction() as session:
        assert get_user_by_email(session, email) is None


def test_get_exist_user_by_id():
    """Test search exists user by email."""
    with mocked_transaction() as session:
        user = add_user(session, fake.name(), fake.email(), fake.password(),
                        fake.address(), fake.latitude(), fake.longitude())
        assert user is not None
        assert get_user_by_id(session, user.id) is not None


def test_get_not_exist_user_by_id():
    """Test search not exists user by email."""
    id = -1  # not_existing_id
    with mocked_transaction() as session:
        assert get_user_by_id(session, id) is None


def test_get_near_users():
    """Test getting all nearby result_users functionality."""
    RADIUS = 2  # KM
    base_coordinates = (32.852310, 35.096149)  # BASE
    in_range_coordinates = [(32.853418, 35.092406),  # 0.37 KM
                            (32.852408, 35.090430),  # 0.54 KM
                            (32.845414, 35.078663),  # 1.81 KM
                            (32.842025, 35.105976),  # 1.47 KM
                            (32.841159, 35.079529)]  # 1.99 KM
    out_of_range_coordinates = [(32.834380, 35.103056),  # 2.09 KM
                                (32.832722, 35.081751),  # 2.56 KM
                                (32.838491, 35.076007),  # 2.43 KM
                                (32.838491, 35.076007),  # 4.72 KM
                                (32.840005, 35.069641)]  # 2.83 KM
    with mocked_transaction() as session:
        in_range_users = [add_user(session, fake.name(), fake.email(),
                                   fake.password(), fake.address(),
                                   coordinate[0], coordinate[1])
                          for coordinate in in_range_coordinates]

        for coordinate in out_of_range_coordinates:
            add_user(session, fake.name(), fake.email(), fake.password(),
                     fake.address(), coordinate[0], coordinate[1])

        # Check that users was added.
        assert len(get_all_users(session)) == len(out_of_range_coordinates) + \
               len(in_range_coordinates)

        result_users = get_near_users(session, latitude=base_coordinates[0],
                                      longitude=base_coordinates[1],
                                      radius=RADIUS)
    assert set(result_users) == set(in_range_users)


def test_update_user_categories():
    """Test update user categories."""
    categories_ids = [1,2,3,4,5,48,201]
    with mocked_transaction() as session:
        user = add_user(session, fake.name(), fake.email(), fake.password(),
                        fake.address(), fake.latitude(), fake.longitude())
        assert user is not None
        update_categories_to_user(session, user.id, categories_ids)
        user = get_user_by_id(session, user.id)
        assert user.categories_ids == categories_ids
