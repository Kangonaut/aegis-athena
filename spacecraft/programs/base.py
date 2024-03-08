import argparse
import abc

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import BasePart, PartStatus
from spacecraft.parts.manager import PartsManager


class ProgramException(Exception):
    pass


class ProgramSyntaxError(ProgramException):
    pass


class ProgramUnsupportedOperation(ProgramException):
    pass


class ProgramKeyError(ProgramException):
    pass


class ProgramValueError(ProgramException):
    pass


class ProgramArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ProgramSyntaxError(message)


class BaseProgram(abc.ABC):
    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        self._parts_manager = parts_manager
        self._display = display

    def _get_part_by_id(self, part_id: str) -> BasePart:
        part = self._parts_manager.get(part_id)
        if part is None:
            raise ProgramKeyError(f"{part_id} is not a valid part ID")
        return part

    @abc.abstractmethod
    def exec(self, arguments: list[str]) -> None:
        pass
