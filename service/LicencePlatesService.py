import dao.LicencePlatesImplementation as LicencePlatesDao


async def getLicencePlates() -> [dict]:
    res = await LicencePlatesDao.getLicencePlates()
    if res is None:
        return {}

    return [dict(item) for item in res]
