from typing import Self
import enum

from .base import BasePart, PartStatus


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


class FuelTank(BasePart):
    def __init__(self, name: str, fuel_type: FuelType, fuel_capacity: float, fuel_content: float):
        super().__init__(name)
        self.__fuel_type = fuel_type
        self.__fuel_capacity: float = fuel_capacity
        self.__fuel_content: float = fuel_content

    def validate(self) -> None:
        if self.__fuel_content > self.__fuel_capacity:
            raise ValueError("the fuel content cannot be greater than the fuel capacity")

    def __str__(self) -> str:
        return f"{self.part_id} - {self.name}"

    @property
    def dependencies(self) -> set[Self]:
        return set()

    @property
    def capacity(self) -> float:
        return self.__fuel_capacity

    @property
    def fuel_type(self) -> FuelType:
        return self.__fuel_type

    @property
    def fuel_content(self) -> float:
        return self.__fuel_content

    def consume_fuel(self, amount: float) -> None:
        self.__fuel_content = max(0.0, self.__fuel_content - amount)

    @property
    def _part_specific_status(self) -> PartStatus:
        if self.__fuel_content <= 0:
            return PartStatus.ERROR
        return PartStatus.NOMINAL
