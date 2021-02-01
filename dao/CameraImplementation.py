from utils.database import fetch, execute


async def getCameras() -> list:
    query = "SELECT * FROM cameras"
    return await fetch(query, isOne=False)
