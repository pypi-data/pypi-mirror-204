
from importlib.abc import Traversable

from importlib.resources import files

# noinspection SpellCheckingInspection
RESOURCES_PACKAGE_NAME: str = 'buildlackey.resources'
VERSION_FILENAME:       str = 'version.txt'


class Version:
    def __init__(self):
        traversable: Traversable = files(RESOURCES_PACKAGE_NAME) / VERSION_FILENAME

        self._version: str = traversable.read_text()

    @property
    def version(self) -> str:
        return self._version
