from typing import Callable

from spacecraft.parts.base import BasePart
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramUnsupportedOperation


class ListProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="list")
    __PARSER.add_argument(
        "subject",
        choices=["parts", "systems"],
        type=str,
    )

    def __handle_list_parts(self) -> None:
        parts: set[BasePart] = self._parts_manager.get_all()
        print(f"{'ID':<10} {'NAME':<30} {'STATUS':<10}")
        for part in parts:
            self._display.print(f"{part.part_id:<10} {part.name:<30} {part.status:<10}")

    def __handle_list_systems(self) -> None:
        raise ProgramUnsupportedOperation("listing all systems is not yet supported")

    def exec(self, arguments: list[str]) -> None:
        arguments = self.__PARSER.parse_args(arguments)

        handlers: dict[str, Callable[[], None]] = {
            "parts": self.__handle_list_parts,
            "systems": self.__handle_list_systems,
        }
        handlers[arguments.subject]()
