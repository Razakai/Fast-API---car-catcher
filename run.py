from fastapi import FastAPI
from routes.v1 import server_v1
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import checkJWTToken
from fastapi.middleware.cors import CORSMiddleware

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
    allow_headers=["authorization", "Authorization" "Accept", "Accept-Language", "Content-Language", "Content-Type"],
    #expose_headers=["*"]
)


@server.middleware("http")
async def middleware(request: Request, callNext):
    if not any(word in str(request.url) for word in ["/login", "/newUser", "/docs", "/openapi.json"]):
        if request.method == "OPTIONS":
            return Response("ok", status_code=200, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true", "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT,DELETE,UPDATE", "Access-Control-Allow-Headers": "Origin,Accept, X-Requested-With, authorization, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"})
        try:
            print("hiii")
            print(request.method)
            print(request.headers["Authorization"])
            jwtToken = request.headers["Authorization"].split(" ")[1] # Authorization
            print(jwtToken)

            if not await checkJWTToken(jwtToken):
                return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await callNext(request)
    return response
