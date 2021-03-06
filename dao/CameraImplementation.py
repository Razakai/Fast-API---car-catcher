from utils.database import fetch, execute
from models.Camera import Camera


async def getCameras() -> list:
    query = "SELECT * FROM cameras"
    return await fetch(query, isOne=False)


async def getCameraByID(cameraID: int) -> list:
    query = "SELECT * FROM cameras WHERE cameraID = :cameraID"
    values = {"cameraID": cameraID}

    return await fetch(query=query, isOne=True, values=values)


async def cameraExists(camera: Camera) -> list:
    query = "SELECT 1 FROM cameras where url = :url"
    values = {"url": camera.url}

    return await fetch(query=query, isOne=True, values=values)


async def createCamera(camera: Camera) -> bool:
    query = "INSERT INTO cameras VALUES(cameraID, :url, :city, :country, :userID)"
    values = {"url": camera.url, "city": camera.city, "country": camera.country, "userID": camera.userID}

    return await execute(query=query, isMany=False, values=values)


async def deleteCamera(cameraID: int) -> bool:
    query = "DELETE FROM cameras WHERE cameraID = :cameraID"
    values = {"cameraID": cameraID}
    return await execute(query=query, isMany=False, values=values)


async def updateCamera(camera: Camera, id: int) -> bool:
    query = """
    UPDATE cameras
    SET url = :url, city = :city, country = :country, userID = :userID
    WHERE cameraID = :cameraID
    """
    values = {"url": camera.url, "city": camera.city, "country": camera.country, "userID": camera.userID, "cameraID": id}
    return await execute(query=query, isMany=False, values=values)