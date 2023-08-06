from jija.drivers import base


class DatabaseDriver(base.Driver):
    async def get_connection(self):
        raise NotImplementedError()

    async def migrate(self):
        raise NotImplementedError()

    async def update(self):
        raise NotImplementedError()
