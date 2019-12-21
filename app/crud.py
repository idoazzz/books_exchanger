"""CRUD operations."""
import hashlib

from app.api_models import UserCreate
from app.db.config import Session
from app.db.models import Category, User


def get_all_categories(session: Session, limit: int = 100):
    """Get all categories from DB."""
    return session.query(Category).limit(limit).all()


def get_categories_by_name(session: Session, filter: str, limit: int = 100):
    """Get all categories that match to specific filter from DB."""
    return session.query(Category).filter(
        Category.name.contains(filter)).limit(limit).all()


def get_all_users(session: Session, limit: int = 100):
    """Get all users from DB."""
    return session.query(User).limit(limit).all()


def get_users_by_name(session: Session, filter: str, limit: int = 100):
    """Get all users that match to specific filter from DB."""
    return session.query(User).filter(
        User.name.contains(filter)).limit(limit).all()

def add_user(session: Session, user_data: UserCreate):
    """Add new user to the DB."""
    new_user = User(name=user_data.name,
                    email=user_data.email,
                    address=user_data.address,
                    password=hashlib.md5(user_data.password.encode()),
                    latitude=user_data.latitude,
                    longitude=user_data.longitude)
    session.add(new_user)
    session.commit()
    # Retrieving new data like generated id.
    session.refresh(new_user)
    return new_user


def get_user_by_email(session: Session, user_data):
    """Get specifc user by email address."""
    return session.query(User).filter_by(email=user_data.email).first()

