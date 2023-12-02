from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.temp_controller import TemperatureController
from spacecraft.parts.water import WaterTank


class EnvironmentController(BasePart):
    def __init__(self, name: str, temperature_controller: TemperatureController, water_tank: WaterTank):
        super().__init__(name)
        self.__temperature_controller = temperature_controller
        self.__water_tank = water_tank

    @property
    def dependencies(self) -> set[Self]:
        return {self.__temperature_controller, self.__water_tank}

    @property
    def temperature_controller(self) -> TemperatureController:
        return self.__temperature_controller

    @property
    def water_tank(self) -> WaterTank:
        return self.__water_tank
