import typing
from typing import Callable, Type
from functools import partial

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.ars import HeatExchanger, ArsController
from spacecraft.parts.base import BasePart, BaseController
from spacecraft.parts.brains_controller import BrainsController
from spacecraft.parts.ecs import EcsController
from spacecraft.parts.hts import CoolingLoop, HtsController
from spacecraft.parts.manager import PartsManager
from spacecraft.parts.coms import Antenna
from spacecraft.parts.coms_controller import ComsController
from spacecraft.parts.oscpcs import OscpcsController
from spacecraft.parts.sps import Engine, SpsController
from spacecraft.parts.eps import FuelCell, EpsController
from spacecraft.parts.wcs import WaterTank, WaterPump, WcsController
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
            BrainsController: {
                "strg": partial(self.__handle_set_part, attribute_name="storage"),
            },
            EcsController: {
                "oscpcs": partial(self.__handle_set_part, attribute_name="oscpcs_controller"),
                "hts": partial(self.__handle_set_part, attribute_name="hts_controller"),
                "wcs": partial(self.__handle_set_part, attribute_name="wcs_controller"),
                "ars": partial(self.__handle_set_part, attribute_name="ars_controller"),
            },
            OscpcsController: {
                "lox": partial(self.__handle_set_part, attribute_name="lox_tank"),
                "ln2": partial(self.__handle_set_part, attribute_name="ln2_tank"),
            },
            HtsController: {
                "therm": partial(self.__handle_set_part, attribute_name="thermometer"),
            },
            CoolingLoop: {
                "rad": partial(self.__handle_set_part, attribute_name="radiator"),
                "pmp": partial(self.__handle_set_part, attribute_name="coolant_pump")
            },
            HeatExchanger: {
                "cool": partial(self.__handle_set_part, attribute_name="cooling_loop")
            },
            ArsController: {
                "fan": partial(self.__handle_set_part, attribute_name="fan"),
                "heatex": partial(self.__handle_set_part, attribute_name="heat_exchanger"),
                "h2osep": partial(self.__handle_set_part, attribute_name="water_seperator"),
                "odorrem": partial(self.__handle_set_part, attribute_name="odor_remover"),
                "co2rem": partial(self.__handle_set_part, attribute_name="co2_remover"),
            },
            WaterPump: {
                "tank": partial(self.__handle_set_part, attribute_name="water_tank"),
            },
            WaterTank: {
                "ws": partial(self.__handle_set_part, attribute_name="water_supply"),
            },
            WcsController: {
                "pmp": partial(self.__handle_set_part, attribute_name="water_pump")
            },
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
                "eng": partial(self.__handle_set_part, attribute_name="engine"),
                "gmbl": partial(self.__handle_set_part, attribute_name="gimbal"),
            },
        }

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
        value_part = self._get_part_by_id(value)
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
        part = self._get_part_by_id(part_id)

        # check if part is controllable
        if not part.controllable:
            raise ProgramValueError(f"part {part_id} does not respond; unable to complete task")

        # call handler
        if key in self.__HANDLERS:
            self.__HANDLERS[key](part, value)
        elif (specific_handlers := self.__PART_SPECIFIC_HANDLERS.get(type(part))) and key in specific_handlers:
            specific_handlers[key](part, value)
        else:
            raise ProgramSyntaxError(f"invalid key: {key}")
