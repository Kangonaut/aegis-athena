import abc
import enum
import random
from typing import Self
from spacecraft import parts_manager


class PartStatus(enum.Enum):
    """
    the status ID are in descending order according to the severity level (0 is the most severe)
    """

    OFFLINE = 1
    ERROR = 2
    NOMINAL = 3

    _ignore_ = ["__COLORS"]
    __COLORS: dict[int, str] = {
        NOMINAL: "green",
        ERROR: "red",
        OFFLINE: "gray",
    }

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    @property
    def color(self) -> str:
        return self.__COLORS[self.value]


class BasePart(abc.ABC):
    def __init__(self, name: str):
        self.__name: str = name
        self.__power_state: bool = True

        # part_id is assigned by the parts manager
        self._part_id: str = ""
        parts_manager.add(self)

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
    @abc.abstractmethod
    def dependencies(self) -> set[Self]:
        pass

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
        If any of the dependencies are in a non-nominal state, the device itself is in state :code:`PartStatus.ERROR`.
        """
        for dependency in self.dependencies:
            if dependency.status != PartStatus.NOMINAL:
                return PartStatus.ERROR
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