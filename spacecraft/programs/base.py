import argparse
import abc

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.manager import PartsManager


class ProgramException(Exception):
    pass


class ProgramSyntaxError(ProgramException):
    pass


class ProgramUnsupportedOperation(ProgramException):
    pass


class ProgramArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ProgramSyntaxError(message)


class BaseProgram(abc.ABC):
    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        self._parts_manager = parts_manager
        self._display = display

    @abc.abstractmethod
    def exec(self, arguments: list[str]) -> None:
        pass
