import random
import time
from typing import Callable, Type, Self

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import BasePart
from spacecraft.parts.brains_controller import BrainsController
from spacecraft.parts.manager import PartsManager
from spacecraft.parts.coms_controller import ComsController
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramKeyError, ProgramValueError


class AskProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="ask")
    __PARSER.add_argument(
        "brains",
        type=str,
    )
    __PARSER.add_argument(
        "message",
        type=str,
        nargs="+",
    )

    __TRANSMIT_DURATION_PER_CHAR: float = 0.05
    __TRANSMIT_MAX_RANDOM_DURATION: float = 0.5
    __RESPONSE_DURATION_PER_CHAR: float = 0.09
    __RESPONSE_MAX_RANDOM_DURATION: float = 3.0

    def __init__(self, parts_manager: PartsManager, display: BaseDisplay):
        super().__init__(parts_manager, display)

    def __assert_controller_type(self, part: BasePart) -> BrainsController:
        if not isinstance(part, BrainsController):
            raise ProgramValueError(f"{part.part_id} must be a BRAINS system")
        return part

    def __generate_response(self, brains_controller: BrainsController, message: str) -> None:
        communicator = brains_controller.communicator
        for token in communicator.stream(message):
            self._display.print(token.content, end="")

        self._display.print("")  # newline

    def exec(self, arguments: list[str]) -> None:
        # transmit 0ab3 "Hello World!"
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.brains
        message: str = " ".join(arguments.message)

        # retrieve part
        part = self._get_part_by_id(part_id)
        brains_controller = self.__assert_controller_type(part)

        self.__generate_response(brains_controller, message)
