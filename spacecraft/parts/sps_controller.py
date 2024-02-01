from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.engine import Engine
from spacecraft.parts.gimbal import EngineGimbal


class SpsController(BasePart):
    def __init__(self, name: str, engine: Engine, gimbal: EngineGimbal):
        super().__init__(name)
        self.engine = engine
        self.gimbal = gimbal

    @property
    def dependencies(self) -> set[Self]:
        return {self.engine, self.gimbal}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"engine: {self.engine.part_id}\n"
                f"gimbal: {self.gimbal.part_id}\n"
        )
