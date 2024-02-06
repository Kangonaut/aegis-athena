import enum
from dataclasses import dataclass
from typing import Self

from spacecraft.communication.communicator import BaseCommunicator
from spacecraft.communication.state import CommunicationState
from spacecraft.communication.dispatcher import BaseCommunicationDispatcher
from spacecraft.parts.base import BasePart, BaseController
from spacecraft.parts.coms import Antenna


class ComsController(BaseController):
    def __init__(self, name: str, antenna: Antenna, secret: str, dispatcher: BaseCommunicationDispatcher):
        super().__init__(name)
        self.antenna = antenna
        self.secret = secret  # ironic, secret is a public attribute :)
        self.dispatcher = dispatcher

    @property
    def dependencies(self) -> set[Self]:
        return {self.antenna}

    def get_communicator(self) -> BaseCommunicator:
        return self.dispatcher.dispatch(
            state=CommunicationState(
                self.antenna,
                self.secret
            )
        )
