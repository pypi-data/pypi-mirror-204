from jija.command import Command
from jija import config


class Migrate(Command):
    async def handle(self):
        await config.DriversConfig.DATABASE.migrate()
