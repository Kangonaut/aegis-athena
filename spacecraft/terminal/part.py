from typing import Callable
import argparse

from spacecraft.parts.base import BasePart
from spacecraft.parts.fuel_cell import FuelCell
from .base import BaseTerminal
from spacecraft import parts_manager
from .fuel_cell import FuelCellTerminal

_SET_PARSER = argparse.ArgumentParser()
_SET_PARSER.add_argument("-i", nargs=1, type=str, required=True)
_SET_PARSER.add_argument("-k", nargs=1, type=str, required=True)
_SET_PARSER.add_argument("-v", nargs=1, type=str, required=True)


class PartTerminal(BaseTerminal):

    @staticmethod
    def handle_set_power(part: BasePart, value: str) -> None:
        parsed_value = bool(int(value))
        if parsed_value:
            part.power_on()
        else:
            part.power_off()

    _SET_KEY_MAPPING: dict[str, Callable[[BasePart, str], None]] = {
        "power": handle_set_power
    }

    @staticmethod
    def handle_set(args: list[str]) -> None:
        parsed_args: argparse.Namespace = _SET_PARSER.parse_args(args)

        # retrieve values
        part_id: str = parsed_args.i[0]
        key: str = parsed_args.k[0]
        value: str = parsed_args.v[0]

        # retrieve part
        part: BasePart | None = parts_manager.get(part_id)

        # add part specific set keys
        set_key_mapping = PartTerminal._SET_KEY_MAPPING
        if isinstance(part, FuelCell):
            set_key_mapping |= FuelCellTerminal.SET_KEY_MAPPING

        # call specific handler
        set_key_mapping[key](part, value)

    # override mappings
    _TERMINAL_MAPPING: dict[str, BaseTerminal] = {}
    _COMMAND_MAPPING: dict[str, Callable[[list[str]], None]] = {
        "set": handle_set,
    }
