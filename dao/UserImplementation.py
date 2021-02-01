from utils.database import fetch, execute
from models.User import User


async def createUser(user: User):
    query = """
        INSERT INTO USERS
        (email, password, first_name, last_name)
        VALUES
        (:email, :password, first_name, :last_name)
    """

    values = {"email": user.email, "password": user.password, "first_name": user.firstName, "last_name": user.lastName}

    res = await execute(query=query, isMany=False, values=values)
    print(res)
