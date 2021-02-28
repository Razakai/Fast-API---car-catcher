import dao.VehicleLocationsDao as LocationsDao
from models.vehicleSighting import VehicleSighting
from service.LicencePlatesService import licencePlateExistsByID
from fastapi import HTTPException
from datetime import datetime


async def createVehicleSighting(vehicleSighting: VehicleSighting) -> bool:
    if await licencePlateExistsByID(vehicleSighting.registrationID):
        #vehicleSighting.DateTime = str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        vehicleSighting.DateTime = datetime.utcnow()
        print(vehicleSighting)
        if await LocationsDao.createVehicleSighting(vehicleSighting):
            return True

        raise HTTPException(status_code=500, detail="Database error")

    raise HTTPException(status_code=409, detail="Registration ID no longer valid")


async def getVehicleLocations() -> [dict]:
    res = await LocationsDao.getVehicleLocations()
    return [dict(item) for item in res]

    '''
    if len(res) > 0:
        res = [dict(item) for item in res]
        idSet = set()
        organisedDict = {}
        for row in res:
            idSet.add(row["plateRegistration"])

        for idNum in idSet:
            organisedDict[idNum] = []

        for row in res:
            organisedDict[row.pop("plateRegistration")].append(row)

        res = organisedDict
    '''
