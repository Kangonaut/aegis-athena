from typing import Self

from spacecraft.parts.base import BasePart, BaseController
from spacecraft.parts.fuel import FuelTank, OxidizerTank
from spacecraft.parts.mock import MockPart


class EngineGimbal(MockPart):
    pass


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


class SpsController(BaseController):
    def __init__(self, name: str, engine: Engine, gimbal: EngineGimbal):
        super().__init__(name)
        self.engine = engine
        self.gimbal = gimbal

    @property
    def dependencies(self) -> set[Self]:
        return {self.engine, self.gimbal}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"engine: {self.engine.part_id}\n"
                f"gimbal: {self.gimbal.part_id}\n"
        )
