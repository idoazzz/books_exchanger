"""Books service app."""
from fastapi import FastAPI, Depends, HTTPException

from .db.tables import Base
from .db.config import transaction, engine


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Initiating DB."""
    Base.metadata.create_all(engine)
