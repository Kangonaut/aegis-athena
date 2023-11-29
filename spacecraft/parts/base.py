import abc
import enum
import random
from typing import Self


class _PartsManager:
    def __init__(self):
        self.parts: dict[str, "BasePart"] = dict()

    @staticmethod
    def __generate_random_part_id() -> str:
        # generate random 2 byte number
        rand_number: int = random.randint(0, 2 ** 16 - 1)

        # convert to hex string with two digits
        rand_hex: str = "{:04x}".format(rand_number)
        return rand_hex

    def __generate_unique_part_id(self):
        # generate part IDs until a unique one is found
        while (part_id := self.__generate_random_part_id()) in self.parts:
            pass
        return part_id

    def add(self, part: "BasePart"):
        # assign part id
        part._part_id = self.__generate_unique_part_id()

        # add part
        self.parts[part.part_id] = part


# singleton
parts_manager = _PartsManager()


class PartStatus(enum.Enum):
    OFFLINE = 1
    ERROR = 2
    NOMINAL = 3

    _ignore_ = ["__COLORS"]
    __COLORS: dict[int, str] = {
        NOMINAL: "green",
        ERROR: "red",
        OFFLINE: "gray",
    }

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

        # self.dependencies: set[BasePart] = set()
        # self.dependants: set[BasePart] = set()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def part_id(self) -> str:
        return self._part_id

    @abc.abstractmethod
    def dependencies(self) -> set[Self]:
        pass

    @property
    def status(self) -> PartStatus:
        if not self.__power_state:
            return PartStatus.OFFLINE

    def power_on(self) -> None:
        self.__power_state = True

    def power_off(self) -> None:
        self.__power_state = False

    @property
    def power_state(self) -> bool:
        return self.__power_state
