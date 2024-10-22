from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.mock import MockPart


class GraphicsProcessingUnit(MockPart):
    pass


class StorageMedium(BasePart):
    def __init__(self, name, capacity: int):
        super().__init__(name)
        self.capacity = capacity

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"capacity: {self.capacity:,} B".replace(",", " ")
        )


class StorageArray(StorageMedium):
    def __init__(self, name, storage_elems: list[StorageMedium]):
        total_capacity = sum(map(lambda x: x.capacity, storage_elems))
        super().__init__(name, total_capacity)
        self.storage_elems = storage_elems

    @property
    def dependencies(self) -> set[Self]:
        return set(self.storage_elems)



