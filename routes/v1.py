from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from service import CamersService, LicencePlatesService, VehicleLocationsService, UserService
from models.User import User
from models.jwtUser import JWTUser
from models.Camera import Camera
from models.LicencePlate import LicencePlate
from models.vehicleSighting import VehicleSighting
from utils.security import authenticateUser, createJWTToken

server_v1 = FastAPI()


# get
@server_v1.get("/cameras")
async def getCameras():
    cameras = await CamersService.getAllCameras()
    return {"cameras": cameras}


@server_v1.get("/sightings")
async def getVehicleSightings():
    sightings = await VehicleLocationsService.getVehicleLocations()
    return {"sightings": sightings}


@server_v1.get("/licencePlates")
async def getLicencePlates():
    licencePlates = await LicencePlatesService.getLicencePlates()
    return {"LicencePlates": licencePlates}


# post
@server_v1.post("/newUser", status_code=HTTP_201_CREATED)
async def createUser(user: User):
    await UserService.createUser(user)
    return {"status": "Created"}


@server_v1.post("/camera", status_code=HTTP_201_CREATED)
async def createCamera(request: Request, camera: Camera):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await CamersService.createCamera(camera, jwtToken)
    return {"status": "Created"}


@server_v1.post("/licencePlate", status_code=HTTP_201_CREATED)
async def createLicencePlate(request: Request, licencePlate: LicencePlate):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await LicencePlatesService.createLicencePlate(licencePlate, jwtToken)
    return {"status": "Created"}


@server_v1.post("/sighting", status_code=HTTP_201_CREATED)
async def createVehicleSighting(vehicleSighting: VehicleSighting):
    await VehicleLocationsService.createVehicleSighting(vehicleSighting)
    return {"status": "Created"}


@server_v1.post("/login")
async def loginForAccessToken(form_data: OAuth2PasswordRequestForm = Depends()):
    jwtUserDict = {"email": form_data.username, "password": form_data.password}
    jwtUser = JWTUser(**jwtUserDict)

    user = await authenticateUser(jwtUser)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = createJWTToken(user)
    return {"token": jwt_token}


# delete
@server_v1.delete("/user")
async def deleteUser(request: Request):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await UserService.deleteUser(jwtToken)
    return {"status": "User deleted"}


@server_v1.delete("/camera/{id}")
async def deleteCamera(request: Request, id: int):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await CamersService.deleteCamera(jwtToken, id)
    return {"status": "Camera deleted"}


@server_v1.delete("/licencePlate/{id}")
async def deleteCamera(request: Request, id: int):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await LicencePlatesService.deleteLicencePlate(jwtToken, id)
    return {"status": "Licence plate deleted"}


@server_v1.put("/licencePlate/{id}")
async def updateLicencePlate(request: Request, id: int, licencePlate: LicencePlate):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await LicencePlatesService.updateLicencePlate(jwtToken, id, licencePlate)
    return {"status": "Licence plate updated"}


@server_v1.put("/camera/{id}")
async def updateCamera(request: Request, id: int, camera: Camera):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await CamersService.updateCamera(jwtToken, id, camera)
    return {"status": "Camera updated"}


@server_v1.put("/user/{id}")
async def updateUser(request: Request, id: int, user: User):
    jwtToken = request.headers["Authorization"].split(" ")[1]
    await UserService.updateUser(jwtToken, user, id)
    return {"status": "User updated"}

