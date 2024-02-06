import abc
from typing import Callable

from spacecraft.builder import SpacecraftBuilder
from spacecraft.displays.base import BaseDisplay
from spacecraft.spacecraft import Spacecraft


class BaseCompletionChecker(abc.ABC):
    @abc.abstractmethod
    def check_completion(self, spacecraft: Spacecraft) -> bool:
        pass


class LevelState:
    def __init__(self,
                 level: "Level",
                 spacecraft: Spacecraft,
                 completion_checker: BaseCompletionChecker) -> None:
        self.level = level
        self.spacecraft = spacecraft
        self.completion_checker = completion_checker

    def is_complete(self) -> bool:
        return self.completion_checker.check_completion(self.spacecraft)


class Level:
    def __init__(self,
                 name: str,
                 prolog: str,
                 epilog: str,
                 completion_checker: BaseCompletionChecker,
                 adjust_spacecraft: Callable[[Spacecraft], None],
                 init_spacecraft: Callable[[BaseDisplay], Spacecraft] = SpacecraftBuilder().build_default) -> None:
        self.name = name
        self.prolog = prolog
        self.epilog = epilog
        self.completion_checker = completion_checker
        self.adjust_spacecraft = adjust_spacecraft
        self.init_spacecraft = init_spacecraft

    def init_level_state(self, display: BaseDisplay) -> LevelState:
        spacecraft = self.init_spacecraft(display)
        self.adjust_spacecraft(spacecraft)

        return LevelState(self, spacecraft, self.completion_checker)
