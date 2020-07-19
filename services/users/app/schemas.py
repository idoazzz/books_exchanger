"""Categories API endpoints models."""
from enum import Enum

from pydantic import BaseModel


class NewUserRequest(BaseModel):
    """User request."""
    email: str
    name: str
    address: str
    password: str
    password2: str
    latitude: int
    longitude: int


class UserAuthenticationRequest(BaseModel):
    """User authentication request."""
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    address: str
    latitude: float
    longitude: float


class UserRequestType(str, Enum):
    id = "id"
    email = "email"
