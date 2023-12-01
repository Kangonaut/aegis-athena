from typing import Callable, Type, Self

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.antenna import Antenna
from spacecraft.parts.base import BasePart
from spacecraft.parts.eps_controller import EpsController
from spacecraft.parts.fuel import FuelTank
from spacecraft.parts.fuel_cell import FuelCell
from spacecraft.parts.manager import PartsManager
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramUnsupportedOperation, ProgramValueError, \
    ProgramKeyError, ProgramSyntaxError


class DetailsProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="details")
    __PARSER.add_argument(
        "part",
        type=str,
    )

    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        super().__init__(parts_manager, display)

        self.__HANDLERS: dict[type, Callable[[any], None]] = {
            FuelCell: self.__handle_fuel_cell,
            Antenna: self.__handle_antenna,
            FuelTank: self.__handle_fuel_tank,
            EpsController: self.__handle_eps_controller,
        }

    def __get_part_by_id(self, part_id: str) -> BasePart:
        part = self._parts_manager.get(part_id)
        if part is None:
            raise ProgramKeyError(f"{part_id} is not a valid part ID")
        return part

    def __describe_basics(self, part: BasePart):
        self._display.print(f"id: {part.part_id}")
        self._display.print(f"name: {part.name}")
        self._display.print(f"status: {part.status}")

    def __handle_fuel_cell(self, part: FuelCell):
        self.__describe_basics(part)
        self._display.print(f"lh2: {part.hydrogen_fuel_tank.part_id}")
        self._display.print(f"lox: {part.oxygen_fuel_tank.part_id}")

    def __handle_antenna(self, part: Antenna):
        self.__describe_basics(part)
        self._display.print(f"range: {part.range_type}")
        self._display.print(f"frequency: {part.frequency} Hz")
        self._display.print(f"frequency_range: {part.frequency_range.min} - {part.frequency_range.max} Hz")

    def __handle_fuel_tank(self, part: FuelTank):
        self.__describe_basics(part)
        self._display.print(f"capacity: {part.capacity} l")
        self._display.print(f"content: {part.fuel_content} l")

    def __handle_eps_controller(self, part: EpsController):
        self.__describe_basics(part)
        self._display.print(f"fuel_cell: {part.fuel_cell.part_id}")
        self._display.print(f"battery: {part.battery.part_id}")

    def __handle_generic_part(self, part: BasePart):
        self.__describe_basics(part)

    def exec(self, arguments: list[str]) -> None:
        # details 0ab3
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.part

        # retrieve part
        part = self.__get_part_by_id(part_id)

        if handler := self.__HANDLERS.get(type(part)):
            handler(part)
        else:
            self.__handle_generic_part(part)
