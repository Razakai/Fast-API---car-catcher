import dao.UserImplementation as UserDao
from models.User import User
from fastapi import HTTPException
from utils.security import getHashedPassword
from utils.security import getEmailFromJWTToken
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


async def createUser(user: User) -> User:
    if not await userExists(user.email):
        user.password = getHashedPassword(user.password)
        user.userID = await UserDao.createUser(user)
        return user

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


async def updateUser(token: str, user: User, id: int) -> User:
    email = getEmailFromJWTToken(token)
    currentUser = await getUserByEmail(email)
    if currentUser["userID"] == id:
        if currentUser["password"] == user.password:
            if user.newPassword != None: # set new password
                user.password = getHashedPassword(user.newPassword)
            else: # use current password
                user.password = getHashedPassword(user.password)
            if await UserDao.updateUser(user, id):
                user.userID = id
                return user

            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update user")

        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User password does not match match")

    raise HTTPException(status_code=HTTP_409_CONFLICT, detail="A user can only edit their own details")


async def getUser(token: str) -> dict:
    email = getEmailFromJWTToken(token)
    return await getUserByEmail(email)


