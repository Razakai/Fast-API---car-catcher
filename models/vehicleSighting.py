from pydantic import BaseModel
from fastapi import Query


class VehicleSighting(BaseModel):
    city: str = Query(..., min_length=2, regex="[a-zA-Z]")
    country: str = Query(..., min_length=2, regex="[a-zA-Z]")
    registrationID: int
    DateTime: str = Query(default=None)
