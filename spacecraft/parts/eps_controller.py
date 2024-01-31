from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.battery import Battery
from spacecraft.parts.fuel_cell import FuelCell


class EpsController(BasePart):
    def __init__(self, name: str, battery: Battery, fuel_cell: FuelCell):
        super().__init__(name)
        self.__battery = battery
        self.__fuel_cell = fuel_cell

    @property
    def dependencies(self) -> set[Self]:
        return {self.__battery, self.__fuel_cell}

    @property
    def battery(self) -> Battery:
        return self.__battery

    @property
    def fuel_cell(self) -> FuelCell:
        return self.__fuel_cell
