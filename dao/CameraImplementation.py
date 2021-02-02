from utils.database import fetch, execute
from models.Camera import Camera


async def getCameras() -> list:
    query = "SELECT * FROM cameras"
    return await fetch(query, isOne=False)


async def cameraExists(camera: Camera) -> bool:
    query = "SELECT 1 FROM cameras where url = :url"
    values = {"url": camera.url}

    return False if await fetch(query=query, isOne=True, values=values) is None else True
