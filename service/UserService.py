import dao.UserImplementation as UserDao
from models.User import User
from fastapi import HTTPException
from utils.security import getHashedPassword


async def createUser(user: User) -> bool:
    if await userExists(user.email):
        user.password = getHashedPassword(user.password)
        return await UserDao.createUser(user)
    else:
        raise HTTPException(status_code=409, detail="Duplicate User")


async def userExists(email: str) -> bool:
    res = await UserDao.userExists(email)
    return True if res is None else False


async def getUserByEmail(email: str) -> dict:
    res = await UserDao.getUserByEmail(email)
    return dict(res)

