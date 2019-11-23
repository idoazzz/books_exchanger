"""Describing exahnger API models."""
from pydantic import BaseModel


class NewUser(BaseModel):
    """New user request model."""
    name: str
    password: str
    email: str
    lat: float
    lan: float
    address: str

