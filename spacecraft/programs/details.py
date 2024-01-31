from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import BasePart
from spacecraft.parts.manager import PartsManager
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramKeyError


class DetailsProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="details")
    __PARSER.add_argument(
        "part",
        type=str,
    )

    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        super().__init__(parts_manager, display)

    def __get_part_by_id(self, part_id: str) -> BasePart:
        part = self._parts_manager.get(part_id)
        if part is None:
            raise ProgramKeyError(f"{part_id} is not a valid part ID")
        return part

    def __describe_basics(self, part: BasePart):
        self._display.print(f"id: {part.part_id}")
        self._display.print(part.display_details())

    def __handle_generic_part(self, part: BasePart):
        self.__describe_basics(part)

    def exec(self, arguments: list[str]) -> None:
        # details 0ab3
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.part

        # retrieve part
        part = self.__get_part_by_id(part_id)
        self.__handle_generic_part(part)
