from models.LicencePlate import LicencePlate
from utils.security import getEmailFromJWTToken
from service.UserService import getUserByEmail
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import dao.LicencePlatesImplementation as LicencePlateDao


async def getLicencePlates() -> [dict]:
    res = await LicencePlateDao.getLicencePlates()
    return [dict(item) for item in res]


async def createLicencePlate(licencePlate: LicencePlate, token: str) -> bool:
    email = getEmailFromJWTToken(token)
    user = await getUserByEmail(email)
    licencePlate.userID = user["userID"]
    if not await licencePlateExists(licencePlate.plateRegistration):
        return await LicencePlateDao.createLicencePlate(licencePlate)
    else:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Duplicate Licence plate")


async def licencePlateExists(registrationNum: str) -> bool:
    return False if await LicencePlateDao.licencePlateExists(registrationNum) is None else True


async def licencePlateExistsByID(id: int) -> bool:
    return False if await LicencePlateDao.licencePlateExistsByID(id) is None else True


async def getLicencePlateByID(id: int) -> dict:
    res = await LicencePlateDao.getLicencePlateByID(id)
    if res is not None:
        return dict(res)

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Camera does not exist")


async def deleteLicencePlate(token: str, licencePlateID: int) -> bool:
    email = getEmailFromJWTToken(token)
    user = await getUserByEmail(email)
    licencePlate = await getLicencePlateByID(licencePlateID)
    if licencePlate["userID"] == user["userID"]:
        if await LicencePlateDao.deleteLicencePlate(licencePlateID):
            return True

        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete licence plate")

    raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Licence plate does not belong to current user")

