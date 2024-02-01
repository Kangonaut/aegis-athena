from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.battery import Battery
from spacecraft.parts.fuel_cell import FuelCell


class EpsController(BasePart):
    def __init__(self, name: str, battery: Battery, fuel_cell: FuelCell):
        super().__init__(name)
        self.battery = battery
        self.fuel_cell = fuel_cell

    @property
    def dependencies(self) -> set[Self]:
        return {self.battery, self.fuel_cell}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"battery: {self.battery.part_id}\n"
                f"fuel cell: {self.fuel_cell.part_id}\n"
        )
