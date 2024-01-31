import abc
from typing import Self

from spacecraft.parts.base import BasePart, PartStatus


class BaseTank(BasePart):
    def __init__(self, name: str, contents: str, contents_abbreviation: str | None, capacity: float, fill_level: float):
        super().__init__(name)
        self.__contents: str = contents
        self.__contents_abbreviation: str | None = contents_abbreviation
        self.__capacity: float = capacity
        self.__fill_level: float = fill_level

    def validate(self) -> None:
        if self.__fill_level > self.__capacity:
            raise ValueError("the fill level cannot be greater than the capacity")

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"contents: {self.contents_abbreviation}\n"
                f"capacity: {self.__capacity} l\n"
                f"fill_level: {self.__fill_level} l\n"
        )

    @property
    def dependencies(self) -> set[Self]:
        return set()

    @property
    def contents(self) -> str:
        return self.__contents

    @property
    def contents_abbreviation(self) -> str:
        return self.__contents_abbreviation or self.__contents

    @property
    def capacity(self) -> float:
        return self.__capacity

    @property
    def fill_level(self) -> float:
        return self.__fill_level

    def consume(self, amount: float) -> None:
        self.__fill_level = max(0.0, self.__fill_level - amount)

    @property
    def _part_specific_status(self) -> PartStatus:
        if self.__fill_level <= 0:
            return PartStatus.MALFUNCTION
        return PartStatus.NOMINAL
