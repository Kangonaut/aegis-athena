import enum
from dataclasses import dataclass
from typing import Self

from spacecraft.communication.communicator import BaseCommunicator
from spacecraft.communication.state import ComsState
from spacecraft.communication.dispatcher import BaseComsDispatcher
from spacecraft.parts.base import BaseController
from spacecraft.parts.coms import Antenna


class ComsController(BaseController):
    def __init__(self, name: str, antenna: Antenna, secret: str, dispatcher: BaseComsDispatcher) -> None:
        super().__init__(name)
        self.antenna = antenna
        self.secret = secret  # ironic, secret is a public attribute :)
        self.dispatcher = dispatcher

    @property
    def dependencies(self) -> set[Self]:
        return {self.antenna}

    @property
    def communicator(self) -> BaseCommunicator:
        return self.dispatcher.dispatch(
            state=ComsState(
                self.antenna,
                self.secret
            )
        )

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"antenna: {self.antenna.part_id}\n"
        )
