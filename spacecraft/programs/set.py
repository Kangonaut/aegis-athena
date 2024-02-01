import typing
from typing import Callable, Type
from functools import partial

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.antenna import Antenna
from spacecraft.parts.base import BasePart
from spacecraft.parts.coms_controller import ComsController
from spacecraft.parts.eps_controller import EpsController
from spacecraft.parts.engine import Engine
from spacecraft.parts.fuel_cell import FuelCell
from spacecraft.parts.manager import PartsManager
from spacecraft.parts.sps_controller import SpsController
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
            "pwr": self.__handle_set_power,
        }
        self.__PART_SPECIFIC_HANDLERS: dict[Type, dict[str, Callable[[any, str], None]]] = {
            FuelCell: {
                "lox": partial(self.__handle_set_part, attribute_name="lox_tank"),
                "lh2": partial(self.__handle_set_part, attribute_name="lh2_tank"),
            },
            Engine: {
                "fuel": partial(self.__handle_set_part, attribute_name="fuel_tank"),
                "oxi": partial(self.__handle_set_part, attribute_name="oxidizer_tank"),
            },
            Antenna: {
                "hz": partial(self.__handle_set_int, attribute_name="frequency"),
            },
            ComsController: {
                "pwd": partial(self.__handle_set_str, attribute_name="secret"),
                "ant": partial(self.__handle_set_part, attribute_name="antenna"),
            },
            EpsController: {
                "fc": partial(self.__handle_set_part, attribute_name="fuel_cell"),
                "bat": partial(self.__handle_set_part, attribute_name="battery"),
            },
            SpsController: {
                "engine": partial(self.__handle_set_part, attribute_name="engine"),
                "gimbal": partial(self.__handle_set_part, attribute_name="gimbal"),
            },
        }

    def __get_part_by_id(self, part_id: str) -> BasePart:
        part = self._parts_manager.get(part_id)
        if part is None:
            raise ProgramKeyError(f"{part_id} is not a valid part ID")
        return part

    def __assert_setter_type(self, part: BasePart, value: BasePart, attribute_name: str) -> None:
        # if public attribute
        type_hints = typing.get_type_hints(part.__init__)
        print(f"type: {part}; type_hints: {type_hints}")
        if attribute_name in type_hints:
            target_type = type_hints[attribute_name]
        # if private attribute with setter
        elif (part_property := getattr(part, attribute_name, None)) and isinstance(part_property, property):
            target_type = typing.get_type_hints(part_property.fset)["value"]
        else:
            raise ProgramValueError(f"{value.part_id} is not compatible")

        # check if types match
        if not isinstance(value, target_type):
            print(f"type: {type(value)}; target: {target_type}")
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

    def __handle_set_part(self, part: BasePart, value: str, attribute_name: str) -> None:
        value_part = self.__get_part_by_id(value)
        self.__assert_setter_type(part, value_part, attribute_name)
        setattr(part, attribute_name, value_part)

    def __handle_set_int(self, part: BasePart, value: str, attribute_name: str) -> None:
        print(attribute_name)
        try:
            value = int(value)
            setattr(part, attribute_name, value)
        except ValueError:
            raise ProgramValueError(f"{attribute_name} must be a valid integer")

    def __handle_set_str(self, part: BasePart, value: str, attribute_name: str):
        setattr(part, attribute_name, value)

    def exec(self, arguments: list[str]) -> None:
        # set 0ab3 power 0
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.part
        key: str = arguments.key
        value: str = arguments.value

        # retrieve part
        part = self.__get_part_by_id(part_id)

        print(part.__class__.__dict__)

        # call handler
        if key in self.__HANDLERS:
            self.__HANDLERS[key](part, value)
        elif (specific_handlers := self.__PART_SPECIFIC_HANDLERS.get(type(part))) and key in specific_handlers:
            specific_handlers[key](part, value)
        else:
            raise ProgramSyntaxError(f"invalid key: {key}")
