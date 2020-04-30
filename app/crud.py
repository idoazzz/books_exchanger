"""CRUD operations."""
import hashlib

from sqlalchemy import asc
from sqlalchemy import func

from app.db.config import Session
from app.db.models import Category, User, Book


# Categories CRUD

def get_all_categories(session: Session, limit: int = 100):
    """Get all categories from DB."""
    return session.query(Category).limit(limit).all()


def get_categories_by_name(session: Session, filter: str, limit: int = 100):
    """Get all categories that match to specific filter from DB."""
    return session.query(Category).filter(
        Category.name.contains(filter)).limit(limit).all()


# Users CRUD


def get_all_users(session: Session, limit: int = 100):
    """Get all users from DB."""
    return session.query(User).limit(limit).all()


def get_users_by_name(session: Session, filter: str, limit: int = 100):
    """Get all users that match to specific filter from DB."""
    return session.query(User).filter(
        User.name.contains(filter)).limit(limit).all()


def get_user_by_email(session: Session, email):
    """Get specifc user by email address."""
    return session.query(User).filter_by(email=email).first()


def get_near_users(session: Session, latitude, longitude, radius):
    """Get all users in range of radius km."""
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


def get_near_users_books(session: Session, latitude, longitude, radius):
    """Get all users in range of radius km."""
    users_in_range = session.query(User).join(Book).filter(func.acos(
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


def add_user(session: Session, password: str, name: str, email: str,
             address: str, latitude: int, longitude: int):
    """Add new user to the DB."""
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
