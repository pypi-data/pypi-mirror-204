import asyncio
import signal
import subprocess
import sys

from jija import config
from jija.command import Command
from jija import reloader


class Run(Command):
    def __init__(self):
        super().__init__()
        self.close_event = asyncio.Event()
        self.reloader = reloader.Reloader(config.StructureConfig.PROJECT_PATH, self.close_event)
        self.runner = None
        self.alive = True

        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, sig, frame):
        self.alive = False
        self.close_event.set()

    async def run_watcher(self):
        await self.reloader.wait()

    async def handle(self):
        asyncio.create_task(self.run_watcher())
        while self.alive:
            self.runner = subprocess.Popen([config.StructureConfig.PYTHON_PATH, 'main.py', 'runprocess'])
            self.close_event.clear()
            await self.close_event.wait()

            self.close_sub_process()
            print()

    def close_sub_process(self):
        if sys.platform == "win32":
            self.runner.send_signal(signal.SIGTERM)
        else:
            self.runner.send_signal(signal.SIGINT)

    def run(self):
        try:
            super().run()
        except KeyboardInterrupt:
            self.reloader.close()
            self.close_sub_process()
            self.runner.wait()
