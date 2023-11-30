from typing import Self

from .base import BasePart, PartStatus
from .fuel import FuelTank, FuelType
from spacecraft import event


class FuelCell(BasePart):
    def __init__(self, name: str):
        super().__init__(name)
        self.__oxygen_fuel_tank: FuelTank | None = None
        self.__hydrogen_fuel_tank: FuelTank | None = None

    def validate(self) -> None:
        if self.__oxygen_fuel_tank.fuel_type != FuelType.LIQUID_OXYGEN:
            raise ValueError("the oxygen fuel tank must have fuel-type oxygen")
        if self.__hydrogen_fuel_tank.fuel_type != FuelType.LIQUID_HYDROGEN:
            raise ValueError("the hydrogen fuel tank must have fuel-type hydrogen")

    @property
    def dependencies(self) -> set[Self]:
        return {self.__oxygen_fuel_tank, self.__hydrogen_fuel_tank}

    @property
    def oxygen_fuel_tank(self) -> FuelTank | None:
        return self.__oxygen_fuel_tank

    @oxygen_fuel_tank.setter
    def oxygen_fuel_tank(self, value: FuelTank) -> None:
        if value.fuel_type != FuelType.LIQUID_OXYGEN:
            raise ValueError("fuel tank must have fuel-type oxygen")
        self.__oxygen_fuel_tank = value
        event.send(event.EventType.PART_CONFIG_UPDATED, None)

    @property
    def hydrogen_fuel_tank(self) -> FuelTank | None:
        return self.__hydrogen_fuel_tank

    @hydrogen_fuel_tank.setter
    def hydrogen_fuel_tank(self, value: FuelTank) -> None:
        if value.fuel_type != FuelType.LIQUID_HYDROGEN:
            raise ValueError("fuel tank must have fuel-type hydrogen")
        self.__hydrogen_fuel_tank = value
        event.send(event.EventType.PART_CONFIG_UPDATED, None)
