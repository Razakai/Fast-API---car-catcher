from utils.database import execute, fetch


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
