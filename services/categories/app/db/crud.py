"""Categories CRUD db operations."""
from .tables import Category


def insert_new_category(session, name: str):
    """Insert new category to DB.

    Args:
        session (Session): Current DB session.
        name (str): Category name.
    """
    session.add(Category(name=name.strip()))


def get_all_categories(session):
    """Get all categories from DB.

    Args:
        session (Session): Current DB session.
        limit (int): Returned categories amount.

    Returns:
        list. Fetched categories.
    """
    return session.query(Category).all()


def get_categories_by_name(session, filter: str):
    """Get all categories that match to specific filter from DB.
    Args:
        filter (str): Contains filter.
        session (Session): Current DB session.
        limit (int): Returned categories amount.

    Returns:
        list. Filtered categories.
    """
    return session.query(Category).filter(Category.name.contains(filter)).all()
