from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from service import CamersService, LicencePlatesService, JWTUserService, VehicleLocationsService, UserService
from models.User import User
from models.jwtUser import JWTUser
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
    return{"sightings": sightings}


@server_v1.get("/licencePlates")
async def getLicencePlates():
    licencePlates = await LicencePlatesService.getLicencePlates()
    return {"LicencePlates": licencePlates}


# post
@server_v1.post("/user", status_code=HTTP_201_CREATED)
async def createUser(user: User):
    await UserService.createUser(user)
    return {"request body": user}


@server_v1.post("/login")
async def loginForAccessToken(form_data: OAuth2PasswordRequestForm = Depends()):
    jwtUserDict = {"email": form_data.username, "password": form_data.password}
    jwtUser = JWTUser(**jwtUserDict)

    user = await authenticateUser(jwtUser)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = createJWTToken(user)
    return {"token": jwt_token}
