import os

import aiohttp_swagger
from aiohttp import web

from jija.contrib.swagger import views
from jija.drivers import DocsDriver


class SwaggerDriver(DocsDriver):
    STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(aiohttp_swagger.__file__), "swagger_ui3"))

    def __init__(self, url: str = '/docs'):
        self.__url = url.rstrip('/')

    @property
    def url(self) -> str:
        return self.__url

    def setup(self, aiohttp_app: web.Application) -> web.Application:
        aiohttp_app.router.add_route('GET', f'{self.url}/', aiohttp_swagger._swagger_home)
        aiohttp_app.router.add_route(
            'GET', f"{self.url}/swagger.json", views.swagger_view)

        static_route = f'{self.url}/swagger_static'

        aiohttp_app.router.add_static(static_route, self.STATIC_PATH)

        aiohttp_app["SWAGGER_DEF_CONTENT"] = 'asdasd'
        self.__set_template(aiohttp_app)
        return aiohttp_app

    def __set_template(self, aiohttp_app: web.Application):
        static_route = f'{self.url}/swagger_static'

        with open(os.path.join(self.STATIC_PATH, "index.html"), "r") as file:
            index_html = file.read()

        aiohttp_app["SWAGGER_TEMPLATE_CONTENT"] = (
            index_html
            .replace("##SWAGGER_CONFIG##", f"{self.url}/swagger.json")
            .replace("##STATIC_PATH##", f"{static_route}")
            .replace("##SWAGGER_VALIDATOR_URL##", "")
        )
