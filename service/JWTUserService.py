import dao.JWTUserImplementation as JWTDao


async def isUserPresentByEmail(email: str) -> bool:
    res = await JWTDao.isUserPresentByEmail(email)

    if res is None:
        return {}
    return res


async def getUserByEmail(user: JWTDao) -> dict:
    res = await JWTDao.getUserByEmail(user)
    if res is None:
        return {}
    return dict(res)
