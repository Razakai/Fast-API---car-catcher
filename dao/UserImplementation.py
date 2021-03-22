from utils.database import fetch, execute
from models.User import User


async def createUser(user: User) -> bool:
    query = """
        INSERT INTO users
        VALUES
        (userID, :email, :password, :first_name, :last_name)
    """

    values = {"email": user.email, "password": user.password, "first_name": user.firstName, "last_name": user.lastName}
    return await execute(query=query, isMany=False, values=values)


async def userExists(email: str) -> list:
    query = "SELECT 1 FROM users WHERE email = :email"
    values = {"email": email}

    return await fetch(query=query, isOne=True, values=values)


async def getUserByEmail(email: str) -> list:
    query = "SELECT userID, email, first_name, last_name, password from users WHERE email = :email"
    values = {"email": email}
    return await fetch(query=query, isOne=True, values=values)


async def deleteUser(email: str) -> bool:
    query = "DELETE FROM users WHERE email = :email"
    values = {"email": email}
    return await execute(query=query, isMany=False, values=values)


async def updateUser(user: User, id: int) -> bool:
    query = """
    UPDATE users
    SET password = :password, first_name = :first_name, last_name = :last_name
    WHERE userID = :userID
    """
    values = {"password": user.password, "first_name": user.firstName, "last_name": user.lastName, "userID": id}
    return await execute(query=query, isMany=False, values=values)

