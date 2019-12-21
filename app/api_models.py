"""Describing exahnger API models."""
from pydantic import BaseModel


class NewUser(BaseModel):
    """New user request model."""
    name: str
    email: str
    address: str
    password: str
    latitude: float
    longitude: float

