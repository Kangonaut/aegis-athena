from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.fuel import LoxTank, Ln2Tank


class OscpcsController(BasePart):
    def __init__(self, name: str, lox_tank: LoxTank, ln2_tank: Ln2Tank):
        super().__init__(name)
        self.lox_tank = lox_tank
        self.ln2_tank = ln2_tank

    def dependencies(self) -> set[Self]:
        return {self.ln2_tank, self.lox_tank}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"LOX: {self.lox_tank.part_id}\n"
                f"LN2: {self.ln2_tank.part_id}\n"
        )
