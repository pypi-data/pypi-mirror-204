from pathlib import Path

from jija import app


class BaseApp(app.App):
    @classmethod
    def cls_get_import_path(cls, path: Path, to: str) -> str:
        return f'jija.base_app.{to}'
