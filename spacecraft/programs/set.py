import typing
from typing import Callable, Type

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.antenna import Antenna
from spacecraft.parts.base import BasePart
from spacecraft.parts.communication_controller import CommunicationController
from spacecraft.parts.fuel import FuelTank
from spacecraft.parts.fuel_cell import FuelCell
from spacecraft.parts.manager import PartsManager
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramValueError, ProgramKeyError, \
    ProgramSyntaxError


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

    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        super().__init__(parts_manager, display)

        self.__HANDLERS: dict[str, Callable[[BasePart, str], None]] = {
            "power": self.__handle_set_power,
        }
        self.__PART_SPECIFIC_HANDLERS: dict[Type, dict[str, Callable[[any, str], None]]] = {
            FuelCell: {
                "lox": self.__handle_fuel_cell_set_oxygen,
                "lh2": self.__handle_fuel_cell_set_hydrogen,
            },
            FuelTank: {},
            Antenna: {
                "hz": self.__handle_antenna_set_frequency,
            },
            CommunicationController: {
                "secret": self.__handle_communication_controller_set_secret,
                "antenna": self.__handle_communication_controller_set_antenna,
            },
        }

    def __get_part_by_id(self, part_id: str) -> BasePart:
        part = self._parts_manager.get(part_id)
        if part is None:
            raise ProgramKeyError(f"{part_id} is not a valid part ID")
        return part

    def __assert_setter_type(self, part_property: property, value: BasePart) -> None:
        target_type = typing.get_type_hints(part_property.fset)["value"]
        if not isinstance(value, target_type):
            raise ProgramValueError(f"{value.part_id} is not compatible")

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

    def __handle_fuel_cell_set_oxygen(self, part: FuelCell, value: str):
        tank = self.__get_part_by_id(value)
        self.__assert_setter_type(part.__class__.oxygen_fuel_tank, tank)
        part.oxygen_fuel_tank = tank

    def __handle_fuel_cell_set_hydrogen(self, part: FuelCell, value: str):
        tank = self.__get_part_by_id(value)
        self.__assert_setter_type(part.__class__.hydrogen_fuel_tank, tank)
        part.hydrogen_fuel_tank = tank

    def __handle_antenna_set_frequency(self, part: Antenna, value: str):
        try:
            value = int(value)
        except ValueError:
            raise ProgramValueError("frequency must be an integer")
        part.frequency = value

    def __handle_communication_controller_set_secret(self, part: CommunicationController, value: str):
        part.secret = value

    def __handle_communication_controller_set_antenna(self, part: CommunicationController, value: str):
        antenna = self.__get_part_by_id(value)
        self.__assert_setter_type(part.__class__.antenna, antenna)
        part.antenna = antenna

    def exec(self, arguments: list[str]) -> None:
        # set 0ab3 power 0
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.part
        key: str = arguments.key
        value: str = arguments.value

        # retrieve part
        part = self.__get_part_by_id(part_id)

        # call handler
        if key in self.__HANDLERS:
            self.__HANDLERS[key](part, value)
        elif (specific_handlers := self.__PART_SPECIFIC_HANDLERS.get(type(part))) and key in specific_handlers:
            specific_handlers[key](part, value)
        else:
            raise ProgramSyntaxError(f"invalid key: {key}")
