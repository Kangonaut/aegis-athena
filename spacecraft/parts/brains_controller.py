from typing import Self

from spacecraft.communication.communicator import BaseCommunicator
from spacecraft.communication.dispatcher import BaseBrainsDispatcher
from spacecraft.communication.state import BrainsState
from spacecraft.parts.base import BaseController
from spacecraft.parts.brains import GraphicsProcessingUnit, StorageMedium


class BrainsController(BaseController):
    def __init__(self, name: str, gpus: list[GraphicsProcessingUnit], storage: StorageMedium,
                 dispatcher: BaseBrainsDispatcher):
        super().__init__(name)
        self.gpus = gpus
        self.storage = storage
        self.dispatcher = dispatcher

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

    @property
    def communicator(self) -> BaseCommunicator:
        return self.dispatcher.dispatch(
            state=BrainsState(
                gpus=self.gpus,
                storage=self.storage,
            )
        )
