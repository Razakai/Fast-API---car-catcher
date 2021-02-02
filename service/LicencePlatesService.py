import dao.LicencePlatesImplementation as LicencePlatesDao


async def getLicencePlates() -> [dict]:
    res = await LicencePlatesDao.getLicencePlates()
    return [dict(item) for item in res]
