from typing import Self

from spacecraft.parts.base import BasePart
from spacecraft.parts.gpu import GraphicsProcessingUnit
from spacecraft.parts.storage import StorageMedium


class BrainsController(BasePart):
    def __init__(self, name: str, gpus: list[GraphicsProcessingUnit], storage: StorageMedium):
        super().__init__(name)
        self.gpus = gpus
        self.storage = storage

    @property
    def dependencies(self) -> set[Self]:
        return {self.storage, *self.gpus}

    def display_details(self) -> str:
        gpu_list: str = " ".join(map(lambda x: x.part_id, self.gpus))
        return (
            super().display_details() +
            f"gpus: {gpu_list}\n"
            f"storage: {self.storage.part_id}\n"
        )
