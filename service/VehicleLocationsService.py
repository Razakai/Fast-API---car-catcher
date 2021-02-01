import dao.VehicleLocationsDao as LocationsDao


async def getVehicleLocations() -> [dict]:
    res = await LocationsDao.getVehicleLocations()
    res = [dict(item) for item in res]
    return res

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
