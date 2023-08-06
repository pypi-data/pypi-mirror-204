from aiohttp import web


class Driver:
    def setup(self, aiohttp_app: web.Application):
        return aiohttp_app

    async def preflight(self):
        pass
