from jija.config import base


class DevConfig(base.Config):
    RELOADER_EXCLUDED_DIRS: set = None

    def __init__(self, *, reloader_excluded=None):
        self.__class__.__PREF = {
            'RELOADER_EXCLUDED_DIRS': reloader_excluded if reloader_excluded else set()
        }

        super().__init__()

    @classmethod
    async def freeze(cls):
        from jija import config

        validated_data = set(
            str(config.StructureConfig.PROJECT_PATH.joinpath(path).absolute())
            for path in cls.__PREF['RELOADER_EXCLUDED_DIRS']
        )

        cls.set_values({
            'RELOADER_EXCLUDED_DIRS': validated_data
        })
