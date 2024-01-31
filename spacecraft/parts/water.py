import abc
from typing import Self

from spacecraft.parts.base import BasePart, PartStatus
from spacecraft.parts.tank import BaseTank


class BaseWaterSupply(BasePart):
    pass


class WaterTank(BaseTank):
    def __init__(self, name: str, capacity: float, fill_level: float, water_supply: BaseWaterSupply):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents="water",
            contents_abbreviation="H2O",
        )
        self.__water_supply: BaseWaterSupply = water_supply

    @property
    def dependencies(self) -> set[Self]:
        return {self.__water_supply}
