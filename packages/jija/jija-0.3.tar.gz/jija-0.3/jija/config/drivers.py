from aiohttp import web

from jija.config import base
from jija.serializers import fields
from jija import drivers


class DriversConfig(base.Config):
    DOCS: drivers.DocsDriver = fields.InstanceField(
        instance_pattern=drivers.DocsDriver,
        required=False,
    )

    DATABASE: drivers.DatabaseDriver = fields.InstanceField(
        instance_pattern=drivers.DatabaseDriver,
        required=False
    )

    def __init__(self, *, docs=None, database=None):
        super().__init__(docs=docs, database=database)

    @classmethod
    def base_app_update(cls, aiohttp_app: web.Application) -> web.Application:
        for item in (cls.DOCS, cls.DATABASE):
            if item:
                aiohttp_app = item.setup(aiohttp_app)

        return aiohttp_app

    @classmethod
    async def preflight(cls):
        for item in (cls.DOCS, cls.DATABASE):
            if item:
                await item.preflight()
