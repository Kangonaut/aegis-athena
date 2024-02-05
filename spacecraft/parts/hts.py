from typing import Self

from spacecraft.parts.base import BasePart, BaseController
from spacecraft.parts.mock import MockPart


class Thermometer(MockPart):
    pass


class Radiator(MockPart):
    pass


class CoolantPump(MockPart):
    pass


class CoolingLoop(BasePart):
    def __init__(self, name: str, radiator: Radiator, coolant_pump: CoolantPump):
        super().__init__(name)
        self.radiator = radiator
        self.coolant_pump = coolant_pump

    @property
    def dependencies(self) -> set[Self]:
        return {self.radiator, self.coolant_pump}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"radiator: {self.radiator}\n"
                f"pump: {self.coolant_pump}\n"
        )


class HtsController(BaseController):
    def __init__(self, name: str, thermometer: Thermometer, cooling_loop: CoolingLoop):
        super().__init__(name)
        self.thermometer = thermometer
        self.cooling_loop = cooling_loop

    @property
    def dependencies(self) -> set[Self]:
        return {self.thermometer, self.cooling_loop}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"thermometer: {self.thermometer.part_id}\n"
                f"loop: {self.cooling_loop.part_id}\n"
        )
