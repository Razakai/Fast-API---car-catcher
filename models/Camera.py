from pydantic import BaseModel
from fastapi import Query


class Camera(BaseModel):
    url: str = Query(..., min_length=5)
    city: str = Query(..., min_length=3)
    country: str = Query(..., min_length=3)
    userID: int = Query(default=None)
