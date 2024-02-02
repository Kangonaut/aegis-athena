from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.mock import MockPart


class Radiator(MockPart):
    pass


class CoolingLoop(BasePart):
    def __init__(self, name: str, radiator: Radiator):
        super().__init__(name)
        self.radiator = radiator

    @property
    def dependencies(self) -> set[Self]:
        return {self.radiator}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"radiator: {self.radiator}\n"
        )
