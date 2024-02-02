from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.water import WaterPump


class WcsController(BasePart):
    def __init__(self, name: str, water_pump: WaterPump):
        super().__init__(name)
        self.water_pump: WaterPump = water_pump

    @property
    def dependencies(self) -> set[Self]:
        return {self.water_pump}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"pump: {self.water_pump.part_id}"
        )
