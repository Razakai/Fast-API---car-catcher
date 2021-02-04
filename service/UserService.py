import dao.UserImplementation as UserDao
from models.User import User
from fastapi import HTTPException
from utils.security import getHashedPassword
from utils.security import getEmailFromJWTToken


async def createUser(user: User) -> bool:
    if not await userExists(user.email):
        user.password = getHashedPassword(user.password)
        return await UserDao.createUser(user)

    raise HTTPException(status_code=409, detail="Duplicate User")


async def userExists(email: str) -> bool:
    res = await UserDao.userExists(email)
    return False if res is None else True


async def getUserByEmail(email: str) -> dict:
    res = await UserDao.getUserByEmail(email)
    return dict(res)


async def deleteUser(token: str) -> bool:
    email = getEmailFromJWTToken(token)

    if await UserDao.deleteUser(email):
        return True

    raise HTTPException(status_code=401, detail="User already deleted")


