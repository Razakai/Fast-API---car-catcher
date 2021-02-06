from utils.database import execute, fetch
from models.vehicleSighting import VehicleSighting


async def getVehicleLocations() -> list:
    query = """
    select
    vehicleLocations. *, vehicleRegistrations.plateRegistration
    from vehicleLocations
    join
    vehicleRegistrations
    on
    vehicleLocations.registrationID = vehicleRegistrations.registrationID
    """
    return await fetch(query=query, isOne=False)


async def createVehicleSighting(vehicleSighting: VehicleSighting) -> bool:
    query = """
    INSERT INTO vehicleLocations
    VALUES(locationID, :city, :country, :time, :registrationID)
    """
    values = {"city": vehicleSighting.city, "country": vehicleSighting.country, "registrationID": vehicleSighting.registrationID, "time": vehicleSighting.DateTime}

    return await execute(query=query, isMany=False, values=values)
