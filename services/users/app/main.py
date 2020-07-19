"""Categories service app."""
import re

from fastapi import FastAPI, Depends, HTTPException
from starlette.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                              HTTP_200_OK)

from .db.tables import Base
from .db.config import transaction, engine
from .schemas import (NewUserRequest, UserResponse, UserRequestType,
                      UserAuthenticationRequest)
from .db.crud import (add_user, get_user_by_email, get_user_by_id,
                      is_authenticated_user, delete_user)

Base.metadata.create_all(engine)

app = FastAPI()


def is_valid_email(email):
    """Validate email."""
    regex = r'[\w\.-]+@[\w\.-]+(\.[\w]+)+'
    if re.search(regex, email):
        return True
    return False


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

    if user_data.password != user_data.password2:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Password are not matching.")

    user = get_user_by_email(session, user_data.email)
    if user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is already taken.")

    user = add_user(session, user_data.password, user_data.name,
                    user_data.email,
                    user_data.address, user_data.latitude, user_data.longitude)
    return {"user_id": user.id}


@app.delete("/delete_user", status_code=HTTP_200_OK)
def remove_user(user_data: UserAuthenticationRequest,
                session=Depends(transaction)):
    """Deleting existing user from DB.

    Args:
        session (Session): DB Session.
        user_data (UserAuthenticationRequest): User email and password.
    """
    if not is_valid_email(user_data.email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Email is invalid.")

    if not delete_user(session, user_data.email, user_data.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="User is not exists.")


@app.get("/users/{request_type}/{key}", response_model=UserResponse)
def search_user_by_id(request_type: UserRequestType, key: str,
                      session=Depends(transaction)):
    """Get users from the db with optional filter.

    Args:
        key (str): User search key.
        session (Session): DB session.
        request_type (UserRequestType): Search by email or user id.

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
