from fastapi import APIRouter
from fastapi import HTTPException
from pydantic.errors import EmailError
from pydantic.utils import validate_email
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.db.models import User
from app.api_models import NewUser
from app.db.config import transaction

router = APIRouter()


@router.post("/add_user", status_code=HTTP_201_CREATED)
def add_user(user_data: NewUser):
    """Adding new user to DB.

    Args:
        user_data (NewUser): New user target data.
    """
    try:
        validate_email(user_data.email)

    except EmailError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is invalid.")

    with transaction() as session:
        users = session.query(User).filter_by(email=user_data.email).all()
        if users:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="Email is already used.")

        session.add(User(admin=False, name=user_data.name,
                    password=user_data.password, email=user_data.email,
                    latitude=user_data.latitude, longitude=user_data.longitude,
                    address=user_data.address))
        session.commit()

@router.get("/users")
def get_users(filter: str = None):
    """Get users from the db with optional filter.

    Args:
        filter (str): Optional filter for the users.

    Notes:
        Filtering the users with naive contains.

    Returns:
        dict. Filtered users.
    """
    with transaction() as session:
        if filter is not None:
            users = session.query(User).filter(
                User.name.contains(filter)).all()
        else:
            users = session.query(User).all()

    return {"users": users}