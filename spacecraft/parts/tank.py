import abc
from typing import Self

from spacecraft.parts.base import BasePart, PartStatus


class BaseTank(BasePart):
    def __init__(self, name: str, capacity: float, content: float):
        super().__init__(name)
        self.__capacity: float = capacity
        self.__content: float = content

    def validate(self) -> None:
        if self.__content > self.__capacity:
            raise ValueError("the content cannot be greater than the capacity")

    @property
    def dependencies(self) -> set[Self]:
        return set()

    @property
    def capacity(self) -> float:
        return self.__capacity

    @property
    def content(self) -> float:
        return self.__content

    def consume(self, amount: float) -> None:
        self.__content = max(0.0, self.__content - amount)

    @property
    def _part_specific_status(self) -> PartStatus:
        if self.__content <= 0:
            return PartStatus.MALFUNCTION
        return PartStatus.NOMINAL
