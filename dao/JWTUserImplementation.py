from models.jwtUser import JWTUser
from utils.database import fetch, execute


async def getUserByEmail(user: JWTUser) -> list:
    query = "SELECT * from users WHERE email = :email"
    values = {"email": user.email}
    return await fetch(query=query, isOne=True, values=values)


async def isUserPresentByEmail(email: str) -> list:
    query = "SELECT * from users WHERE email = :email"
    values = {"email": email}
    return await fetch(query=query, isOne=True, values=values)
