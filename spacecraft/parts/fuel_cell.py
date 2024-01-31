from typing import Self

from spacecraft.parts.fuel import LoxTank, Lh2Tank
from .water import BaseWaterSupply


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
