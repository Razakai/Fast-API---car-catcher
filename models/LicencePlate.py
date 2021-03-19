from pydantic import BaseModel
from fastapi import Query


class LicencePlate(BaseModel):
    registrationID: int = Query(default=None)
    plateRegistration: str = Query(..., min_length=5)
    userID: int = Query(default=None)
