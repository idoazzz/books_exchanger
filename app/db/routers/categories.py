from fastapi import APIRouter

from app.db.models import Category
from app.db.config import transaction

router = APIRouter()

@router.get("/categories")
def get_categories(filter: str = None):
    """Get categories from the db with optional filter.

    Args:
        filter (str): Optional filter for the categories.

    Notes:
        Filtering the categories with naive contains.

    Returns:
        dict. Filtered categories.
    """
    with transaction() as session:
        if filter is not None:
            categories = session.query(Category).filter(
                Category.name.contains(filter)).all()
        else:
            categories = session.query(Category).all()

    categories_names = list(map(lambda element: str(element.name), categories))
    return {"categories": categories_names}
