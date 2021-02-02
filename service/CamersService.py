import dao.CameraImplementation as CameraDao
from models.Camera import Camera
from utils.security import getEmailFromJWTToken
from service.UserService import getUserByEmail
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT


async def getAllCameras() -> [dict]:
    res = await CameraDao.getCameras()

    return [dict(item) for item in res]


async def createCamera(camera: Camera, token: str) -> bool:
    email = getEmailFromJWTToken(token)
    user = await getUserByEmail(email)
    camera.userID = user["userID"]
    if not await cameraExists(camera):
        return await CameraDao.createCamera(camera)
    else:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Duplicate Camera")


async def cameraExists(camera: Camera) -> bool:
    return False if await CameraDao.cameraExists(camera) is None else True
