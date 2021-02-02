from passlib.context import CryptContext
from models.jwtUser import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import time
import service.JWTUserService as JWTUserService

passwordContext = CryptContext(schemes=["bcrypt"])
oauthSchema = OAuth2PasswordBearer(tokenUrl="/token")


def getHashedPassword(password):
    return passwordContext.hash(password)


def verifyPassword(password, hashPassword):
    try:
        return passwordContext.verify(password, hashPassword)
    except Exception as e:
        return False


# Authenticate username and password to give JWT token
async def authenticateUser(user: JWTUser):
    validUser = await JWTUserService.getUserByEmail(user)

    if validUser != {} and verifyPassword(user.password, validUser["password"]):
        return user
    return None


# Create access JWT token
def createJWTToken(user: JWTUser):
    exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": user.email,
        "exp": exp,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Check weather JWT token is correct
async def checkJWTToken(token: str = Depends(oauthSchema)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        email = payload.get("sub")
        exp = payload.get("exp")

        if time.time() < exp:

            if await JWTUserService.isUserPresentByEmail(email):
                return True

        return False
    except Exception as e:
        return False


def getEmailFromJWTToken(token: str = Depends(oauthSchema)):
    return jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM).get("sub")
