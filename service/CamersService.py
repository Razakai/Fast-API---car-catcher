import dao.CameraImplementation as CameraDao
from models.Camera import Camera
from utils.security import getEmailFromJWTToken
from service.UserService import getUserByEmail
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


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


async def getCameraByID(cameraID: int) -> dict:
    res = await CameraDao.getCameraByID(cameraID)
    if res is not None:
        return dict(res)

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Camera does not exist")


async def deleteCamera(token: str, cameraID: int) -> bool:
    email = getEmailFromJWTToken(token)
    user = await getUserByEmail(email)
    camera = await getCameraByID(cameraID)
    if camera["userID"] == user["userID"]:
        if await CameraDao.deleteCamera(cameraID):
            return True

        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete camera")

    raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Camera does not belong to current user")
