from pydantic import BaseModel


class JWTUser(BaseModel):
    email: str
    password: str
