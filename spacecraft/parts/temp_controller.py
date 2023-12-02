from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.cooler import Cooler
from spacecraft.parts.thermometer import Thermometer


class TemperatureController(BasePart):
    def __init__(self, name: str, cooler: Cooler, thermometer: Thermometer):
        super().__init__(name)
        self.__cooler = cooler
        self.__thermometer = thermometer

    @property
    def dependencies(self) -> set[Self]:
        return {self.__cooler, self.__thermometer}

    @property
    def cooler(self) -> Cooler:
        return self.__cooler

    @property
    def thermometer(self) -> Thermometer:
        return self.__thermometer
