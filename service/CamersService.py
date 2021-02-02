import dao.CameraImplementation as CameraServiceDao
from models.Camera import Camera
from utils.security import getEmailFromJWTToken
from service.UserService import userExists


async def getAllCameras() -> [dict]:
    res = await CameraServiceDao.getCameras()

    return [dict(item) for item in res]


async def createCamera(camera: Camera, token: str):
    email = getEmailFromJWTToken(token)
    if await userExists(email):
        pass


async def cameraExists(camera: Camera) -> bool:
    return await CameraServiceDao.cameraExists(camera)
