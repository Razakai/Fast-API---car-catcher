from fastapi import FastAPI
from routes.v1 import server_v1
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import checkJWTToken

server = FastAPI()

server.mount("/v1", server_v1)


@server.middleware("http")
async def middleware(request: Request, callNext):
    if not any(word in str(request.url) for word in ["/login", "/newUser", "/docs", "/openapi.json"]):
        try:
            jwtToken = request.headers["Authorization"].split(" ")[1]

            if not await checkJWTToken(jwtToken):
                return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await callNext(request)
    return response
