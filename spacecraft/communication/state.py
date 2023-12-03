from dataclasses import dataclass

from spacecraft.parts.antenna import Antenna


@dataclass
class CommunicationState:
    """
    Represents the state that the communication system is in.
    """
    antenna: Antenna
    secret: str
