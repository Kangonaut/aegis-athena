import abc
import enum
import random
from typing import Self


class PartException(Exception):
    pass


class PartInvalidConfiguration(PartException):
    pass


class PartStatus(enum.Enum):
    """
    the status ID are in descending order according to the severity level (0 is the most severe)
    """

    OFFLINE = 1
    MALFUNCTION = 2
    NOMINAL = 3

    _ignore_ = ["__DISPLAY_NAMES"]
    __DISPLAY_NAMES: dict[Self, str] = {
        OFFLINE: "OFFLINE",
        NOMINAL: "NOMINAL",
        MALFUNCTION: "MALFUNC",
    }

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    def __str__(self):
        return self.__DISPLAY_NAMES[self.value]


class BasePart(abc.ABC):
    def __init__(self, name: str):
        self.__name: str = name
        self.__power_state: bool = True

        # part_id is assigned by the parts manager
        self._part_id: str = ""

    def validate(self) -> None:
        """
        Validate the configuration of the part.
        Raises a corresponding exception if the config is invalid.
        :exception ValueError
        """
        pass

    @property
    def name(self) -> str:
        return self.__name

    @property
    def part_id(self) -> str:
        return self._part_id

    @property
    def dependencies(self) -> set[Self]:
        return set()

    @property
    def __power_status(self) -> PartStatus:
        """
        The part status solely based on the power state (on or off) of the part.
        """
        if not self.__power_state:
            return PartStatus.OFFLINE
        return PartStatus.NOMINAL

    @property
    def __dependency_status(self) -> PartStatus:
        """
        The part status solely based on the dependencies.
        If any of the dependencies are in a non-nominal state, the device itself is in state :code:`PartStatus.MALFUNCTION`.
        """
        for dependency in self.dependencies:
            if dependency.status != PartStatus.NOMINAL:
                return PartStatus.MALFUNCTION
        return PartStatus.NOMINAL

    @property
    def _part_specific_status(self) -> PartStatus:
        """
        The part status solely based on the properties of the specific part.
        """
        return PartStatus.NOMINAL

    @property
    def status(self) -> PartStatus:
        return min(self.__power_status, self.__dependency_status, self._part_specific_status)

    def power_on(self) -> None:
        self.__power_state = True

    def power_off(self) -> None:
        self.__power_state = False

    @property
    def power_state(self) -> bool:
        return self.__power_state
