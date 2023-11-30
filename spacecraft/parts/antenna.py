import enum
from typing import Self

from .base import BasePart


class RangeType(enum.Enum):
    SHORT_RANGE = 1
    LONG_RANGE = 2


class Antenna(BasePart):
    def __init__(self, name: str, range_type: RangeType):
        super().__init__(name)
        self.__range_type = range_type

    @property
    def range_type(self) -> RangeType:
        return self.__range_type

    @property
    def dependencies(self) -> set[Self]:
        return set()
