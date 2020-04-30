"""Users REST endpoints."""
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter
from fastapi import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.db.config import transaction
from app.crud import get_all_users, get_users_by_name, get_user_by_email, \
    add_user

router = APIRouter()


@router.post("/add_user", status_code=HTTP_201_CREATED)
def add_new_user(password: str, name: str, email: str, address: str,
                 latitude: int, longitude: int):
    """Adding new user to DB.

    Args:
        user_data (UserCreate): New user target data.
    """
    try:
        validate_email(email)

    except EmailNotValidError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is invalid.")

    with transaction() as session:
        user = get_user_by_email(session, email)
        if user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="Email is already used.")

        return add_user(session, password, name, email, address, latitude,
                        longitude)


@router.get("/users")
def get_users(filter: str = None, limit: int = 100):
    """Get users from the db with optional filter.

    Args:
        filter (str): Users name filter.

    Notes:
        Filtering the users with naive contains.

    Returns:
        dict. Filtered users.
    """
    with transaction() as session:
        if filter is not None:
            users = get_users_by_name(session, filter, limit)
        else:
            users = get_all_users(session, limit)

    return {"users": users}