import abc
from typing import Callable

from spacecraft.builder import SpacecraftBuilder
from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import PartStatus
from spacecraft.spacecraft import Spacecraft


class BaseCompletionChecker(abc.ABC):
    @abc.abstractmethod
    def check_completion(self, spacecraft: Spacecraft) -> bool:
        pass


class ControllerStatusCompletionChecker(BaseCompletionChecker):
    def check_completion(self, spacecraft: Spacecraft) -> bool:
        return all(part.status == PartStatus.NOMINAL for part in spacecraft.parts_manager.get_controllers())


class Level(abc.ABC):
    name: str
    prolog: str
    epilog: str
    completion_checker: BaseCompletionChecker
    init_spacecraft: Callable[[BaseDisplay], Spacecraft]

    def __init__(self, display: BaseDisplay) -> None:
        self.spacecraft = self.init_spacecraft(display)

    def is_complete(self) -> bool:
        return self.completion_checker.check_completion(self.spacecraft)


class Level0(Level):
    name = "Level 0 - What the f*ck?"
    prolog = "lorem ipsum dolor sit"
    epilog = "lorem ipsum dolor sit"
    completion_checker = ControllerStatusCompletionChecker()
    init_spacecraft = SpacecraftBuilder.build_level_0
