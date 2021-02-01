import dao.CameraImplementation as CameraServiceDao


async def getAllCameras() -> [dict]:
    res = await CameraServiceDao.getCameras()

    return [dict(item) for item in res]
