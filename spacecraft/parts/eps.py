from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.wcs import BaseWaterSupply
from spacecraft.parts.mock import MockPart
from spacecraft.parts.fuel import LoxTank, Lh2Tank


class FuelCell(BaseWaterSupply):
    def __init__(self, name: str, lox_tank: LoxTank, lh2_tank: Lh2Tank):
        super().__init__(name)
        self.lox_tank: LoxTank = lox_tank
        self.lh2_tank: Lh2Tank = lh2_tank

    @property
    def dependencies(self) -> set[Self]:
        return {self.lh2_tank, self.lox_tank}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"LOX: {self.lox_tank.part_id}\n"
                f"LH2: {self.lh2_tank.part_id}\n"
        )


class Battery(MockPart):
    pass


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
