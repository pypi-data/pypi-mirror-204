from jija.command import Command
from jija import config


class Update(Command):
    async def handle(self):
        await config.DriversConfig.DATABASE.update()
