"""Categories REST endpoints."""
from fastapi import APIRouter

from old_app.db.config import transaction
from old_app.crud import get_all_categories, get_categories_by_name

router = APIRouter()

@router.get("/categories")
def get_categories(filter: str = None, limit: int = 100):
    """Get categories from the db with optional filter.

    Args:
        filter (str): Categories name filter.

    Notes:
        Filtering the categories with naive contains.

    Returns:
        dict. Filtered categories.
    """
    with transaction() as session:
        if filter is not None:
            categories = get_categories_by_name(session, filter, limit)
        else:
            categories = get_all_categories(session, limit)

    categories_names = list(map(lambda element: str(element.name), categories))
    return {"categories": categories_names}


