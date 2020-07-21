"""Users CRUD db operations."""
import hashlib

from sqlalchemy import asc

from .tables import User


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


def get_user_by_id(session, id: int):
    """Get all users that match to specific id from DB.

    Args:
        session (Session): DB session.
        id (int): User id.

    Returns:
        list. User objects.
    """
    return session.query(User).filter_by(id=id).first()


def get_user_by_email(session, email: str):
    """Get specific user by email address.

    Args:
        email (str): User email.
        session (Session): DB session.

    Returns:
        User. Founded user.
    """
    return session.query(User).filter_by(email=email).first()


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
    return user is not None


def add_user(session, name: str, email: str, password: str, address: str,
             latitude: int, longitude: int):
    """Add new user to the DB.

    Args:
        email (str): User email.
        name (str): User full name.
        session (Session): DB session.
        address (str): User home address.
        password (str): User (not hashed) password.
        latitude (float): User home address latitude.
        longitude (float): User home address longitude.

    Returns:
        User. New user object.
    """
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    new_user = User(name=name,
                    email=email,
                    address=address,
                    password=hashed_password,
                    latitude=latitude,
                    longitude=longitude,
                    categories_ids=[])

    session.add(new_user)
    session.commit()
    # Retrieving new data like generated id.
    session.refresh(new_user)
    return new_user


def delete_user(session, email: str, password: str):
    """Delete specific user.

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


def _get_distance(base_latitude, base_longitude, target_latitude,
                  target_longitude, logger=None):
    """Get distance between two coordinates.

    Notes:
        Debugging function.
    """
    from math import sin, cos, sqrt, atan2, radians

    if logger:
        logger.debug("Calculating distance between (%f, %f), (%f, %f)",
                     base_latitude, base_longitude, target_latitude,
                     target_longitude)

    R = 6373.0  # approximate radius of earth in km
    lat1 = radians(base_latitude)
    lon1 = radians(base_longitude)
    lat2 = radians(target_latitude)
    lon2 = radians(target_longitude)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def get_near_users(session, latitude: float, longitude: float, radius: int):
    """Get all users in range of radius (KM).

    Args:
        radius (int): Radius in KM.
        session (Session): DB session.
        latitude (float): User home address latitude.
        longitude (float): User home address longitude.

    Returns:
        list. User objects.
    """
    users_in_range = session.query(User).filter(
        User.in_range(latitude, longitude, radius) <=
        radius).order_by(asc(User.in_range(latitude, longitude, radius))).all()
    return users_in_range


def update_categories_to_user(session, user_id, categories_ids):
    """Update categories to specific user.

    Args:
        user_id (int): User id.
        session (Session): DB session.
        categories_ids (list): Categories ids.
    """
    session.query(User).filter(User.id == user_id).update(
        {'categories_ids': categories_ids})
    session.commit()
