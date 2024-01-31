from typing import Self

from spacecraft.parts.base import BasePart

class SpsController(BasePart):
    def __init__(self, name: str, engine: Engine, gimbal: Gimbal):
        super().__init__(name)
        self.__engine = engine
        self.__gimbal = gimbal

    @property
    def dependencies(self) -> set[Self]:
        return {self.__engine, self.__gimbal}

    @property
    def battery(self) -> Battery:
        return self.__battery

    @property
    def fuel_cell(self) -> FuelCell:
        return self.__fuel_cell
