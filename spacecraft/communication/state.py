import abc
from dataclasses import dataclass

from spacecraft.parts.brains import StorageMedium, GraphicsProcessingUnit
from spacecraft.parts.coms import Antenna


class CommunicationState(abc.ABC):
    pass


@dataclass
class ComsState(CommunicationState):
    antenna: Antenna
    secret: str


@dataclass
class BrainsState(CommunicationState):
    storage: StorageMedium
    gpus: list[GraphicsProcessingUnit]
