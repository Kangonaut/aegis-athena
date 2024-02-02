from typing import Self

from spacecraft.parts.base import BasePart
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
        self.water_supply: BaseWaterSupply = water_supply

    @property
    def dependencies(self) -> set[Self]:
        return {self.water_supply}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"supply: {self.water_supply.part_id}\n"
        )


class WaterPump(BasePart):
    def __init__(self, name: str, water_tank: WaterTank):
        super().__init__(name)
        self.water_tank: WaterTank = water_tank

    @property
    def dependencies(self) -> set[Self]:
        return {self.water_tank}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"tank: {self.water_tank.part_id}\n"
        )


class WcsController(BasePart):
    def __init__(self, name: str, water_pump: WaterPump):
        super().__init__(name)
        self.water_pump: WaterPump = water_pump

    @property
    def dependencies(self) -> set[Self]:
        return {self.water_pump}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"pump: {self.water_pump.part_id}"
        )
