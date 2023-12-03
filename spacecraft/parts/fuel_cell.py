from typing import Self

from .base import PartInvalidConfiguration
from .fuel import FuelTank, FuelType
from spacecraft import event
from .water import BaseWaterSupply


class FuelCell(BaseWaterSupply):
    def __init__(self, name: str):
        super().__init__(name)
        self.__oxygen_fuel_tank: FuelTank | None = None
        self.__hydrogen_fuel_tank: FuelTank | None = None

    def validate(self) -> None:
        if self.__oxygen_fuel_tank.fuel_type != FuelType.LIQUID_OXYGEN:
            raise PartInvalidConfiguration("the oxygen fuel tank must have fuel-type oxygen")
        if self.__hydrogen_fuel_tank.fuel_type != FuelType.LIQUID_HYDROGEN:
            raise PartInvalidConfiguration("the hydrogen fuel tank must have fuel-type hydrogen")

    @property
    def dependencies(self) -> set[Self]:
        return {self.__oxygen_fuel_tank, self.__hydrogen_fuel_tank}

    @property
    def oxygen_fuel_tank(self) -> FuelTank | None:
        return self.__oxygen_fuel_tank

    @oxygen_fuel_tank.setter
    def oxygen_fuel_tank(self, value: FuelTank) -> None:
        if value.fuel_type != FuelType.LIQUID_OXYGEN:
            raise PartInvalidConfiguration("fuel tank must have fuel-type oxygen")
        self.__oxygen_fuel_tank = value

    @property
    def hydrogen_fuel_tank(self) -> FuelTank | None:
        return self.__hydrogen_fuel_tank

    @hydrogen_fuel_tank.setter
    def hydrogen_fuel_tank(self, value: FuelTank) -> None:
        if value.fuel_type != FuelType.LIQUID_HYDROGEN:
            raise PartInvalidConfiguration("fuel tank must have fuel-type hydrogen")
        self.__hydrogen_fuel_tank = value
