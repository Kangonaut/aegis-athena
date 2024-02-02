from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.hts import CoolingLoop
from spacecraft.parts.mock import MockPart


class Fan(MockPart):
    pass


class HeatExchanger(BasePart):
    def __init__(self, name: str, cooling_loop: CoolingLoop):
        super().__init__(name)
        self.cooling_loop = cooling_loop

    @property
    def dependencies(self) -> set[Self]:
        return {self.cooling_loop}

    def display_details(self) -> str:
        return (
            super().display_details() +
            f"cooler: {self.cooling_loop.part_id}\n"
        )


class WaterSeparator(MockPart):
    pass


class OdorRemover(MockPart):
    pass


class Co2Remover(MockPart):
    pass


class ArsController(BasePart):
    def __init__(self,
                 name: str,
                 fan: Fan,
                 heat_exchanger: HeatExchanger,
                 water_separator: WaterSeparator,
                 odor_remover: OdorRemover,
                 co2_remover: Co2Remover):
        super().__init__(name)
        self.fan = fan
        self.heat_exchanger = heat_exchanger
        self.water_separator = water_separator
        self.odor_remover = odor_remover
        self.co2_remover = co2_remover

    @property
    def dependencies(self) -> set[Self]:
        return {self.fan, self.heat_exchanger, self.water_separator, self.odor_remover, self.co2_remover}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"fan: {self.fan.part_id}\n"
                f"heat exchanger: {self.heat_exchanger.part_id}\n"
    f"water separator: {self.water_separator.part_id}\n"
                f"odor remover: {self.odor_remover.part_id}\n"
                f"CO2 remover: {self.co2_remover.part_id}\n"
        )
