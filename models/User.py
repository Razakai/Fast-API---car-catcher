from pydantic import BaseModel
from fastapi import Query


class User(BaseModel):
    firstName: str
    lastName: str
    password: str = Query(..., min_length=5)
    # check if email is valid, ... means the parameter is required. can also be set to None
    email: str = Query(..., regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
