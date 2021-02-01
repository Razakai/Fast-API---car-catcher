from utils.database import fetch, execute
from models.User import User


async def createUser(user: User):
    query = """
        INSERT INTO users
        VALUES
        (userID, :email, :password, :first_name, :last_name)
    """

    values = {"email": user.email, "password": user.password, "first_name": user.firstName, "last_name": user.lastName}
    print("values---", values)
    res = await execute(query=query, isMany=False, values=values)
