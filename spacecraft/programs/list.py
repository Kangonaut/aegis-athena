import time
from typing import Callable
import random

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import BasePart, BaseController
from spacecraft.parts.manager import PartsManager
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramUnsupportedOperation


class ListProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="list")
    __PARSER.add_argument(
        "subject",
        choices=["parts", "systems"],
        type=str,
    )

    MIN_PROCESSING_DURATION: float = 0.01
    MAX_PROCESSING_DURATION: float = 0.05

    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        super().__init__(parts_manager, display)

        self.__HANDLERS: dict[str, Callable[[], None]] = {
            "parts": self.__handle_list_parts,
            "systems": self.__handle_list_systems,
        }

    def __handle_list_parts(self) -> None:
        parts: set[BasePart] = self._parts_manager.get_all()
        parts: list[BasePart] = sorted(parts, key=lambda part: part.name)
        for part in parts:
            self._display.print(f"{part.part_id:<10} {part.name:<40} [[ {part.status:<7} ]]")
            self.__simulate_wait_time()

    def __handle_list_systems(self) -> None:
        controllers = self._parts_manager.get_controllers()
        controllers = sorted(controllers, key=lambda controller: controller.name)
        for controller in controllers:
            self._display.print(f"{controller.get_system_name():<51} [[ {controller.status:<7} ]]")
            self.__simulate_wait_time()

    def __simulate_wait_time(self) -> None:
        duration: float = random.uniform(self.MIN_PROCESSING_DURATION, self.MAX_PROCESSING_DURATION)
        time.sleep(duration)

    def exec(self, arguments: list[str]) -> None:
        arguments = self.__PARSER.parse_args(arguments)
        subject: str = arguments.subject

        # call handler
        self.__HANDLERS[subject]()
