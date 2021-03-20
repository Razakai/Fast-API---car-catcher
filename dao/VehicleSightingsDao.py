from utils.database import execute, fetch
from models.vehicleSighting import VehicleSighting


async def getVehicleSightings() -> list:
    query = """
    select
    vehicleSightings. *, vehicleRegistrations.plateRegistration
    from vehicleSightings
    join
    vehicleRegistrations
    on
    vehicleSightings.registrationID = vehicleRegistrations.registrationID
    """
    return await fetch(query=query, isOne=False)


async def createVehicleSighting(vehicleSighting: VehicleSighting) -> bool:
    query = """
    INSERT INTO vehicleSightings
    VALUES(sightingID, :city, :country, :time, :registrationID)
    """
    values = {"city": vehicleSighting.city, "country": vehicleSighting.country, "registrationID": vehicleSighting.registrationID, "time": vehicleSighting.DateTime}

    return await execute(query=query, isMany=False, values=values)
