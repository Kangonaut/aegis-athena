from typing import Callable
from spacecraft.parts.base import BasePart
from spacecraft.parts.fuel_cell import FuelCell
from spacecraft import parts_manager


class FuelCellTerminal:
    @staticmethod
    def handle_set_oxygen_tank(part: FuelCell, value: str) -> None:
        # retrieve oxygen tank
        oxygen_tank: BasePart | None = parts_manager.get(value)

        part.oxygen_fuel_tank = oxygen_tank

    SET_KEY_MAPPING: dict[str, Callable[[FuelCell, any], None]] = {
        "albert": handle_set_oxygen_tank
    }
