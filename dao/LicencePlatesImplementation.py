from utils.database import execute, fetch


async def getLicencePlates() -> list:
    query = "SELECT * FROM vehicleRegistrations"
    return await fetch(query, isOne=False)
