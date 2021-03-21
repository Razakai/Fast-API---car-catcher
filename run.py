from fastapi import FastAPI
from routes.v1 import server_v1
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import checkJWTToken
from fastapi.middleware.cors import CORSMiddleware
from utils.rabbitMQCommunitcation import createConnection, breakConnection
from utils.database import connectDB, disconnectDB

server = FastAPI()

server.mount("/v1", server_v1)

origins = [
    "http://localhost",
    "http://localhost:8080/",
    "http://localhost:8080"
]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["authorization", "Authorization" "Accept", "Accept-Language", "Content-Language", "Content-Type"]
)


@server.middleware("http")
async def middleware(request: Request, callNext):
    if not any(word in str(request.url) for word in ["/login", "/newUser", "/docs", "/openapi.json"]):
        if request.method == "OPTIONS":
            return Response("ok", status_code=200, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true", "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT,DELETE,UPDATE", "Access-Control-Allow-Headers": "Origin,Accept, X-Requested-With, authorization, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"})
        try:
            jwtToken = request.headers["Authorization"].split(" ")[1] # Authorization

            if not await checkJWTToken(jwtToken):
                return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await callNext(request)
    return response

# on startup
@server.on_event("startup")
async def startRabbitConnection():
    createConnection()
    await connectDB()


# on shutdown
@server.on_event("shutdown")
async def stopRabbitConnection():
    breakConnection()
    await disconnectDB()

