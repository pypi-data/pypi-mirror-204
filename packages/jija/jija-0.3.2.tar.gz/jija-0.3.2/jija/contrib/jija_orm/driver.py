from jija.drivers import DatabaseDriver
from jija import config

from jija_orm.migrator import migrator
from jija_orm import config as jija_orm_config


class JijaOrmDriver(DatabaseDriver):
    def __init__(
            self,
            *,
            database: str,
            password: str,
            host: str = 'localhost',
            user: str = 'postgres',
            port: int = 5432
    ):

        super().__init__()

        self.__user = user
        self.__password = password

        self.__host = host
        self.__port = port

        self.__database = database

    @property
    def user(self) -> str:
        return self.__user

    @property
    def password(self) -> str:
        return self.__password

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port

    @property
    def database(self) -> str:
        return self.__database

    async def preflight(self):
        await jija_orm_config.JijaORM.async_init(
            project_dir=config.StructureConfig.PROJECT_PATH,
            connection=jija_orm_config.Connection(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            ),
            apps=self.__get_apps()
        )

    @staticmethod
    def __get_apps():
        from jija_orm import config as jija_orm_config
        from jija.apps import Apps

        apps = []
        for app in Apps.apps.values():
            if app.exist('models.py'):
                path = app.name if app.parent is None else f'apps.{app.name}'
                apps.append(jija_orm_config.App(
                    name=app.name, path=path, migration_dir=app.get_import_path('migrations')))

        return apps

    @classmethod
    async def get_connection(cls):
        pass

    async def migrate(self):
        migrator_instance = migrator.Migrator()
        await migrator_instance.migrate()

    async def update(self):
        migrator_instance = migrator.Migrator()
        await migrator_instance.update()
