from typing import Callable

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import PartInvalidConfiguration
from spacecraft.parts.manager import PartsManager
from spacecraft.programs.ask import AskProgram
from spacecraft.programs.base import BaseProgram, ProgramException, ProgramSyntaxError
from spacecraft.programs.details import DetailsProgram
from spacecraft.programs.list import ListProgram
from spacecraft.programs.set import SetProgram
from spacecraft.programs.transmit import TransmitProgram


class Shell(BaseProgram):
    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        super().__init__(parts_manager, display)

        self.__programs: dict[str, BaseProgram] = {
            "list": ListProgram(parts_manager, display),
            "set": SetProgram(parts_manager, display),
            "details": DetailsProgram(parts_manager, display),
            "transmit": TransmitProgram(parts_manager, display),
            "ask": AskProgram(parts_manager, display),
        }

    @staticmethod
    def error_handler(func: Callable[..., any]) -> Callable[..., any]:
        def wrapper(*args: any, **kwargs: any):
            try:
                func(*args, **kwargs)
            except (ProgramException, PartInvalidConfiguration) as ex:
                # args[0] = self
                args[0].__output_error(ex)

        return wrapper

    @error_handler
    def exec(self, command: str) -> None:
        # output command input
        self._display.print(f"system:/ $ {command}")

        # decompose command into program and args
        command_parts = command.split()
        program: str = command_parts[0]
        arguments: list[str] = command_parts[1:]

        if program in self.__programs:
            self.__programs[program].exec(arguments)
        else:
            raise ProgramSyntaxError(f"program not found: {program}")

    def __output_error(self, error: Exception) -> None:
        self._display.error(str(error))
