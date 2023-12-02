from typing import Self
import enum

from .base import BasePart, PartStatus
from .tank import BaseTank


class FuelType(enum.Enum):
    LIQUID_OXYGEN = 1
    LIQUID_HYDROGEN = 2

    _ignore_ = ["__NAMES", "__ACRONYMS"]
    __NAMES: dict[Self, str] = {
        LIQUID_OXYGEN: "liquid oxygen",
        LIQUID_HYDROGEN: "liquid hydrogen",
    }
    __ACRONYMS: dict[Self, str] = {
        LIQUID_OXYGEN: "LOX",
        LIQUID_HYDROGEN: "LH2",
    }

    @property
    def display_name(self) -> str:
        return self.__NAMES[self.value]

    @property
    def acronym(self) -> str:
        return self.__ACRONYMS[self.value]

    def __str__(self) -> str:
        return self.acronym


class FuelTank(BaseTank):
    def __init__(self, name: str, capacity: float, content: float, fuel_type: FuelType):
        super().__init__(name, capacity, content)
        self.__fuel_type = fuel_type

    @property
    def fuel_type(self) -> FuelType:
        return self.__fuel_type
