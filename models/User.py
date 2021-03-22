from pydantic import BaseModel
from fastapi import Query


class User(BaseModel):
    userID: int = Query(default=None)
    firstName: str = Query(..., min_length=2)
    lastName: str = Query(..., min_length=2)
    password: str = Query(..., min_length=5)
    newPassword: str = Query(default=None, min_length=5)
    # check if email is valid, ... means the parameter is required. can also be set to None
    email: str = Query(default=None, regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
