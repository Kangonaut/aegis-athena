from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.fuel import FuelTank, OxidizerTank


class Engine(BasePart):
    def __init__(self, name: str, fuel_tank: FuelTank, oxidizer_tank: OxidizerTank):
        super().__init__(name)
        self.fuel_tank: FuelTank = fuel_tank
        self.oxidizer_tank: OxidizerTank = oxidizer_tank

    @property
    def dependencies(self) -> set[Self]:
        return {self.fuel_tank, self.oxidizer_tank}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"fuel: {self.fuel_tank.part_id}\n"
                f"oxidizer: {self.oxidizer_tank.part_id}\n"
        )
