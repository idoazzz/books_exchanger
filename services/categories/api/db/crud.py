"""Categories CRUD db operations."""
from api.db.tables import Category

CATEGORIES_LIMIT = 100


def insert_new_category(session, name: str):
    """Insert new category to DB.

    Args:
        session (Session): Current DB session.
        name (str): Category name.
    """
    print(name.strip())
    session.add(Category(name=name.strip()))


def get_all_categories(session, limit: int = CATEGORIES_LIMIT):
    """Get all categories from DB.

    Args:
        session (Session): Current DB session.
        limit (int): Returned categories amount.

    Returns:
        list. Fetched categories.
    """
    return session.query(Category).limit(limit).all()


def get_categories_by_name(session, filter: str,
                           limit: int = CATEGORIES_LIMIT):
    """Get all categories that match to specific filter from DB.
    Args:
        filter (str): Contains filter.
        session (Session): Current DB session.
        limit (int): Returned categories amount.

    Returns:
        list. Filtered categories.
    """
    return session.query(Category).filter(
        Category.name.contains(filter)).limit(limit).all()
