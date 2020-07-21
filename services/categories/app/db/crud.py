"""Categories CRUD db operations."""
from .tables import Category


def insert_new_category(session, name: str):
    """Insert new category to DB.

    Args:
        session (Session): Current DB session.
        name (str): Category name.
    """
    new_category = Category(name=name)
    session.add(new_category)
    session.commit()
    # Retrieving new data like generated id.
    session.refresh(new_category)
    return new_category


def get_all_categories(session):
    """Get all categories from DB.

    Args:
        session (Session): Current DB session.

    Returns:
        list. Fetched categories.
    """
    return session.query(Category).all()


def get_categories_by_name(session, filter: str):
    """Get all categories that match to specific filter from DB.
    Args:
        filter (str): Contains filter.
        session (Session): Current DB session.

    Returns:
        list. Filtered categories.
    """
    return session.query(Category).filter(Category.name.contains(filter)).all()


def get_category_by_id(session, id: int):
    """Get category that matches to specific id from DB.
    Args:
        id (int): Category id.
        session (Session): Current DB session.

    Returns:
        Category. Filtered categories.
    """
    return session.query(Category).filter_by(id=id).first()
