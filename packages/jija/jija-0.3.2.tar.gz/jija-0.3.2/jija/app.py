from typing import Optional, Type

import os

import importlib
from pathlib import Path

from aiohttp import web

from jija.collector import collect_subclasses
from jija.middleware import Middleware
from jija.command import Command
from jija import config
from jija import router


class App:
    CUSTOM_URL_PATH: Optional[str] = None

    def __init__(
            self,
            name: str,
            path: Path,
            parent: Optional['App'],
            app_router: router.Router,
            middlewares: list[Middleware],
            commands: dict[str, Type[Command]],
    ):
        if parent:
            parent.add_child(self)

        self.__name = name
        self.__path = path
        self.__parent = parent
        self.__router = app_router
        self.__middlewares = middlewares
        self.__commands = commands
        self.__childes = []

        self.__aiohttp_app = self.create_aiohttp_app()

    @classmethod
    def construct(
            cls,
            name: str,
            path: Path,
            parent: Optional['App'] = None,
            extends: Optional['App'] = None
    ) -> 'App':

        app_router = cls.get_router(path, parent)
        middlewares = cls.get_middlewares(path)
        commands = cls.get_commands(path)

        if extends:
            app_router = extends.router + app_router
            middlewares = extends.middlewares + middlewares

            _commands = extends.commands.copy()
            _commands.update(commands)

            commands = _commands

        return cls(
            name,
            path,
            parent,
            app_router,
            middlewares,
            commands,
        )

    @property
    def parent(self) -> Optional['App']:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def router(self) -> router.Router:
        return self.__router

    @property
    def middlewares(self) -> list[Middleware]:
        return self.__middlewares

    @property
    def aiohttp_app(self) -> web.Application:
        return self.__aiohttp_app

    @property
    def childes(self) -> list['App']:
        return self.__childes

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def commands(self) -> dict[str, Type[Command]]:
        return self.__commands

    @classmethod
    def get_router(cls, path: Path, parent: Optional['App']) -> "router.Router":
        if not cls.cls_exist(path, 'routes'):
            raw_routes = []

        else:
            import_path = cls.cls_get_import_path(path, 'routes')
            routes_module = importlib.import_module(import_path)

            raw_routes = getattr(routes_module, 'routes', [])

        if parent is None and cls.CUSTOM_URL_PATH is not None:
            raw_routes = [router.Include(cls.CUSTOM_URL_PATH, raw_routes)]

        app_router = router.Router(raw_routes)
        return app_router

    @classmethod
    def get_middlewares(cls, path: Path) -> list[Middleware]:
        if not cls.cls_exist(path, 'middlewares'):
            return []

        import_path = cls.cls_get_import_path(path, 'middlewares')
        middlewares_module = importlib.import_module(import_path)
        middlewares = collect_subclasses(middlewares_module, Middleware)

        return list(map(lambda middleware: middleware(), middlewares))

    @classmethod
    def get_commands(cls, path: Path) -> dict[str, Type[Command]]:
        if not cls.cls_exist(path, 'commands'):
            return {}

        commands = {}
        commands_path = path.joinpath('commands')
        for file in os.listdir(commands_path):
            if file.endswith('.py') and not file.startswith('_'):

                import_path = cls.cls_get_import_path(path, f'commands.{file.removesuffix(".py")}')
                command_module = importlib.import_module(import_path)

                command = list(collect_subclasses(command_module, Command))
                if command:
                    commands[file.replace('.py', '')] = command[0]

        return commands

    @staticmethod
    def is_app(path: Path) -> bool:
        if path.is_dir() is False or path.joinpath('app.py').exists() is False:
            return False

        for part in path.parts:
            if part.startswith('__'):
                return False

        return True

    def create_aiohttp_app(self) -> web.Application:
        aiohttp_app = web.Application()

        aiohttp_app.middlewares.extend(self.middlewares)

        aiohttp_app.add_routes(self.router.routes)
        aiohttp_app['JIJA_ROUTER'] = self.router

        return aiohttp_app

    def add_child(self, child: "App"):
        self.__childes.append(child)

    def get_import_path(self, to: str) -> str:
        return self.cls_get_import_path(self.path, to)

    @staticmethod
    def cls_get_import_path(path: Path, to: str) -> str:
        modify_class_path = path.joinpath(to)
        return ".".join(modify_class_path.relative_to(config.StructureConfig.PROJECT_PATH).parts)

    def exist(self, name: str) -> bool:
        return self.cls_exist(self.path, name)

    @staticmethod
    def cls_exist(path: Path, name: str) -> bool:
        return path.joinpath(name).exists() or path.joinpath(f'{name}.py').exists()

    def register(self):
        for child in self.childes:
            child.register()

            self.aiohttp_app.add_subapp(prefix=child.get_url_prefix(), subapp=child.aiohttp_app)

    def get_url_prefix(self) -> str:
        """
        Method returns app path prefix
        If app is core we returns name or CUSTOM_URL_PATH
        If app is secondary we need to add prefix of first app
            because in core app we make Include if CUSTOM_URL_PATH is defined and app doesn't know itself name
        If app is thirded we returns only it prefix
        """

        if not self.parent:
            return self.CUSTOM_URL_PATH or ''

        self_prefix = self.CUSTOM_URL_PATH or f'/{self.name}'

        if not self.parent.parent:
            parent_prefix = self.parent.get_url_prefix()
        else:
            parent_prefix = ''

        return f'{parent_prefix}{self_prefix}'

    def aiohttp_app_update(self, new_aiohttp_app: web.Application):
        self.__aiohttp_app = new_aiohttp_app
