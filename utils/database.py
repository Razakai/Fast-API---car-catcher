from databases import Database
from utils.const import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD


async def connectDB():
    db = Database(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    await db.connect()
    return db


async def disconnectDB(db):
    await db.disconnect()


async def execute(query, isMany, values=None):  # insert, delete, update
    db = await connectDB()
    if isMany:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    await disconnectDB(db)


async def fetch(query, isOne, values=None) -> list:  # get
    db = await connectDB()
    if isOne:
        res = await db.fetch_one(query=query, values=values)

    else:
        res = await db.fetch_all(query=query, values=values)

    await disconnectDB(db)
    return res
