from pydantic import BaseModel

class CategoryRequest(BaseModel):
    filter: str
    limit: int

class CategoryResponse(BaseModel):
    id: int 
    name: str