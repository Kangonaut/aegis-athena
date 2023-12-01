from typing import Callable

from spacecraft.parts.base import BasePart
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramUnsupportedOperation, ProgramValueError, \
    ProgramKeyError


class SetProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="set")
    __PARSER.add_argument(
        "part",
        type=str,
    )
    __PARSER.add_argument(
        "key",
        type=str,
    )
    __PARSER.add_argument(
        "value",
        type=str,
    )

    def __handle_set_power(self, part: BasePart, value: str) -> None:
        try:
            value = int(value)
            if value == 1:
                part.power_on()
            elif value == 0:
                part.power_off()
            else:
                raise ProgramValueError("value must either be 0 or 1")
        except ValueError:
            raise ProgramValueError("value must be a valid integer")

    def exec(self, arguments: list[str]) -> None:
        # set 0ab3 power 0
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.part
        key: str = arguments.key
        value: str = arguments.value

        # retrieve part
        part = self._parts_manager.get(part_id)
        if part is None:
            raise ProgramKeyError(f"{part_id} is not a valid part ID")

        print(type(part))

        # call handler
        handlers: dict[str, Callable[[BasePart, str], None]] = {
            "power": self.__handle_set_power,
        }
        handlers[key](part, value)
