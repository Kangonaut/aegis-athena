from typing import Self

from spacecraft.communication.communicator import BaseCommunicator
from spacecraft.communication.dispatcher import BaseCommunicationDispatcher
from spacecraft.communication.state import CommunicationState
from spacecraft.parts.antenna import Antenna
from spacecraft.parts.base import BasePart


class ComsController(BasePart):
    def __init__(self, name: str, antenna: Antenna, secret: str, dispatcher: BaseCommunicationDispatcher):
        super().__init__(name)
        self.antenna = antenna
        self.secret = secret  # ironic, secret is a public attribute :)
        self.__dispatcher = dispatcher

    @property
    def dependencies(self) -> set[Self]:
        return {self.antenna}

    def get_communicator(self) -> BaseCommunicator:
        return self.__dispatcher.dispatch(
            state=CommunicationState(
                self.antenna,
                self.secret
            )
        )
