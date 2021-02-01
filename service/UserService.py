import dao.UserImplementation as UserDao
from models.User import User


async def createUser(user: User):
    await UserDao.createUser(user)


