from databases import Database
from utils.const import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

class database():
    def __init__(self):
        self.db = None
    
    async def connectDB(self):
        self.db = Database(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        await self.db.connect()
    
    async def disconnectDB(self):
        await self.db.disconnect()

    async def execute(self, query, isMany, values):
        try:
            if isMany:
                return await self.db.execute_many(query=query, values=values)

            return await self.db.execute(query=query, values=values)

        except Exception as e:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Conflicting database entry")
    
    async def fetch(self, query, isOne, values):
        try:
            if isOne:
                return await self.db.fetch_one(query=query, values=values)

            return await self.db.fetch_all(query=query, values=values)

        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")
    


db = database()

async def connectDB():
    await db.connectDB()

async def disconnectDB():
    await db.disconnectDB()


async def execute(query, isMany, values=None) -> int:  # insert, delete, update
    return await db.execute(query, isMany, values)


async def fetch(query, isOne, values=None) -> list:  # get
    return await db.fetch(query, isOne, values)
