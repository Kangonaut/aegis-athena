from dataclasses import dataclass

from spacecraft.parts.coms import Antenna


@dataclass
class CommunicationState:
    """
    Represents the state that the communication system is in.
    """
    antenna: Antenna
    secret: str
