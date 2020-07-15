"""Categories API endpoints models."""
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    """Category as response."""
    id: int
    name: str
