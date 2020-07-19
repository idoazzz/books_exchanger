"""Categories service app."""
from typing import List
from email.utils import parseaddr

from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_200_OK

from .db.config import transaction, engine
from .db.tables import Base
from .schemas import NewUserRequest, UserResponse, UserRequestType, \
    UserAuthenticationRequest
from .db.crud import add_user, get_user_by_email, get_user_by_id, \
    is_authenticated_user

Base.metadata.create_all(engine)

app = FastAPI()


def is_valid_email(email):
    """Validate email."""
    return '@' in parseaddr(email)[1]


@app.post("/add_user", status_code=HTTP_201_CREATED)
def add_new_user(user_data: NewUserRequest, session=Depends(transaction)):
    """Adding new user to DB.

    Args:
        session (Session): DB session.
        user_data (UserCreate): New user target data.
    """
    if not is_valid_email(user_data.email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is invalid.")

    user = get_user_by_email(session, user_data.email)
    if user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is already taken.")

    user = add_user(session, user_data.password, user_data.name,
                    user_data.email,
                    user_data.address, user_data.latitude, user_data.longitude)
    return {"user_id": 1}


@app.get("/users/{request_type}/{key}", response_model=UserResponse)
def search_user_by_id(request_type: UserRequestType, key: str,
                      session=Depends(transaction)):
    """Get users from the db with optional filter.

    Args:
        key (str): User search key.
        session (Session): DB session.

    Notes:
        Filtering the users with naive contains.
    """
    user = None
    if request_type == UserRequestType.id:
        try:
            id_key = int(key)

        except ValueError:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="ID must by a number.")

        user = get_user_by_id(session, id_key)

    if request_type == UserRequestType.email:
        if not is_valid_email(key):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="Email is invalid.")

        user = get_user_by_email(session, key)

    if user is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="User was not found.")
    return UserResponse(id=user.id, email=user.email, name=user.name,
                        address=user.address, latitude=user.latitude,
                        longitude=user.longitude)


@app.get("/users/{email}", response_model=UserResponse)
def search_user_by_email(email: str, session=Depends(transaction)):
    """Get users from the db with optional filter.

    Args:
        email (str): User email.
        session (Session): DB session.

    Notes:
        Filtering the users with naive contains.
    """
    user = get_user_by_email(session, email)
    if user is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="User was not found.")
    return UserResponse(id=user.id, email=user.email, name=user.name,
                        address=user.address, latitude=user.latitude,
                        longitude=user.longitude)


@app.post("/authenticate_user", status_code=HTTP_200_OK)
def authenticate_user(user_data: UserAuthenticationRequest,
                      session=Depends(transaction)):
    """Authenticate user.

    Args:
        session (Session): DB session.
        user_data (UserAuthenticationRequest): User credentials.
    """
    if not is_valid_email(user_data.email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is invalid.")

    if not is_authenticated_user(session, user_data.email, user_data.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email or password are wrong.")

# @app.on_event("startup")
# async def startup_event():
#     """Initiating DB."""
#     session = Session()
#     init_categories(session=session, engine=engine)
#     session.close()
#
#
# @app.get("/categories", response_model=List[CategoryResponse])
# def get_categories(filter: str = None, session=Depends(transaction)):
#     """Get categories from the DB with optional filter.
#
#     Args:
#         session (Session): DB session.
#         filter (str): Categories name filter.
#
#     Notes:
#         Filtering the categories with naive contains.
#     """
#     if filter is not None:
#         categories = get_categories_by_name(session, filter)
#     else:
#         categories = get_all_categories(session)
#     return [CategoryResponse(id=category.id, name=category.name)
#             for category in categories]
