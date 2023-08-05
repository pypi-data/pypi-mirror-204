
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment


class EnvironmentBase:
    """

    """
    ENV_PROJECTS_BASE: str = 'PROJECTS_BASE'
    ENV_PROJECT:       str = 'PROJECT'

    def __init__(self):

        self.ebLogger: Logger = getLogger(__name__)

        self._projectsBase:     str = ''
        self._projectDirectory: str = ''

        try:
            self._projectsBase = osEnvironment[EnvironmentBase.ENV_PROJECTS_BASE]
        except KeyError:
            self.ebLogger.info(f'Project Base not set')
        try:
            self._projectDirectory = osEnvironment[EnvironmentBase.ENV_PROJECT]
        except KeyError:
            self.ebLogger.info(f'Project Directory not set')

    @property
    def projectsBase(self) -> str:
        return self._projectsBase

    @property
    def projectDirectory(self) -> str:
        return self._projectDirectory

    @property
    def validProjectsBase(self) -> bool:
        if self._projectsBase == '':
            return False
        else:
            return True

    def validProjectDirectory(self) -> bool:
        if self._projectDirectory == '':
            return False
        else:
            return True
