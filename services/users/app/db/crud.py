"""Users CRUD db operations."""
import hashlib

from sqlalchemy import func, asc

from services.users.app.db.tables import User


def get_all_users(session):
    """Get all users from DB.

    Args:
       session (Session): DB session.

    Returns:
        list. User objects.

    Notes:
        Internal endpoint for tests.
    """
    return session.query(User).all()


def get_users_by_name(session, filter: str):
    """Get all users that match to specific filter from DB.

    Args:
        session (Session): DB session.
        filter (str): User name filter.

    Returns:
        list. User objects.
    """
    return session.query(User).filter(User.name.contains(filter)).all()


def get_users_by_email(session, filter: str):
    """Get all users that match to specific filter from DB.

    Args:
        session (Session): DB session.
        filter (str): User email filter.

    Returns:
        list. User objects.
    """
    return session.query(User).filter(User.email.contains(filter)).all()


def get_user_by_email(session, email: str):
    """Get specific user by email address.

    Args:
        email (str): User email.
        session (Session): DB session.

    Returns:
        User. Founded user.
    """
    return session.query(User).filter_by(email=email).first()


def get_near_users(session, latitude: int, longitude: int, radius: int):
    """Get all users in range of radius (KM).

    Args:
        radius (int): Radius in KM.
        session (Session): DB session.
        latitude (int): User home address latitude.
        longitude (int): User home address longitude.

    Returns:
        list. User objects.
    """
    # TODO: Test!
    users_in_range = session.query(User).filter(func.acos(
        func.sin(func.radians(latitude)) * func.sin(
            func.radians(User.latitude)) + func.cos(
            func.radians(latitude)) * func.cos(
            func.radians(User.latitude)) * func.cos(
            func.radians(User.longitude) - (
                func.radians(longitude)))) * 6371 <= radius).order_by(asc(
        func.acos(
            func.sin(func.radians(latitude)) * func.sin(
                func.radians(User.latitude)) + func.cos(
                func.radians(latitude)) * func.cos(
                func.radians(User.latitude)) * func.cos(
                func.radians(User.longitude) - (
                    func.radians(longitude)))) * 6371
    ))
    return users_in_range


def add_user(session, password: str, name: str, email: str, address: str,
             latitude: int, longitude: int):
    """Add new user to the DB.

    Args:
        email (str): User email.
        name (str): User full name.
        session (Session): DB session.
        address (str): User home address.
        password (str): User (not hashed) password.
        latitude (int): User home address latitude.
        longitude (int): User home address longitude.

    Returns:
        User. New user object.
    """
    # TODO: Test!
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    new_user = User(name=name,
                    email=email,
                    address=address,
                    password=hashed_password,
                    latitude=latitude,
                    longitude=longitude)

    session.add(new_user)
    session.commit()
    # Retrieving new data like generated id.
    session.refresh(new_user)
    return new_user


def is_authenticated_user(session, email: str, password: str):
    """Check if the user is authenticated.

    Args:
        email (str): User email.
        session (Session): DB session.
        password (str): User (not hashed) password.

    Returns:
        bool. If the user was found.
    """
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user = session.query(User).filter_by(email=email,
                                         password=hashed_password).first()
    return user is None


def delete_user(session, email: str, password: str):
    """Check if the user is authenticated.

    Args:
        email (str): User email.
        session (Session): DB session.
        password (str): User (not hashed) password.

    Returns:
        bool. If the user was found and deleted or not.
    """
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user = session.query(User).filter_by(email=email,
                                         password=hashed_password).first()
    if user is None:
        return False

    session.delete(user)
    session.commit()
    return True