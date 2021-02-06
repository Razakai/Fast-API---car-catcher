from utils.database import fetch, execute
from models.LicencePlate import LicencePlate


async def getLicencePlates() -> list:
    query = "SELECT * FROM vehicleRegistrations"
    return await fetch(query, isOne=False)


async def createLicencePlate(licencePlate: LicencePlate) -> bool:
    query = "INSERT INTO vehicleRegistrations values(registrationID, :plateRegistration, :userID)"
    values = {"plateRegistration": licencePlate.plateRegistration, "userID": licencePlate.userID}

    return await execute(query=query, isMany=False, values=values)


async def licencePlateExists(registrationNumber: str) -> list:
    query = "SELECT 1 FROM vehicleRegistrations WHERE plateRegistration = :plateRegistration"
    values = {"plateRegistration": registrationNumber}

    return await fetch(query=query, isOne=True, values=values)


async def licencePlateExistsByID(id: int) -> list:
    query = "SELECT 1 FROM vehicleRegistrations WHERE registrationID = :id"
    values = {"id": id}

    return await fetch(query=query, isOne=True, values=values)


async def getLicencePlateByID(id: int) -> list:
    query = "SELECT * FROM vehicleRegistrations WHERE registrationID = :registrationID"
    values = {"registrationID": id}

    return await fetch(query=query, isOne=True, values=values)


async def deleteLicencePlate(id: int) -> bool:
    query = "DELETE FROM vehicleRegistrations WHERE registrationID = :registrationID"
    values = {"registrationID": id}
    return await execute(query=query, isMany=False, values=values)