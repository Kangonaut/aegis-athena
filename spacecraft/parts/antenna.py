import enum
from typing import Self
from dataclasses import dataclass

from spacecraft.parts.base import BasePart, PartInvalidConfiguration


class RangeType(enum.Enum):
    SHORT_RANGE = 1
    LONG_RANGE = 2

    _ignore_ = ["__DISPLAY_NAMES"]
    __DISPLAY_NAMES: dict[Self, str] = {
        SHORT_RANGE: "short range",
        LONG_RANGE: "long range",
    }

    def __str__(self):
        return self.__DISPLAY_NAMES[self.value]


@dataclass
class FrequencyRange:
    min: int
    max: int


class Antenna(BasePart):
    def __init__(self, name: str, range_type: RangeType, frequency: int, frequency_range: FrequencyRange):
        """
        :param name:
        :param range_type: short or long range
        :param frequency: frequency that the antenna is tuned in at in Hz
        :param frequency_range: frequency range [min, max]
        """
        super().__init__(name)
        self.__range_type = range_type
        self.__frequency = frequency
        self.__frequency_range = frequency_range

    @property
    def range_type(self) -> RangeType:
        return self.__range_type

    @property
    def dependencies(self) -> set[Self]:
        return set()

    @property
    def frequency(self) -> int:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: int) -> None:
        if self.__frequency_range.min <= value <= self.__frequency_range.max:
            self.__frequency = value
        else:
            raise PartInvalidConfiguration(
                f"{value} is not inside the antenna's frequency range of [{self.__frequency_range.min}, {self.__frequency_range.max}]"
            )

    @property
    def frequency_range(self) -> FrequencyRange:
        return self.__frequency_range
