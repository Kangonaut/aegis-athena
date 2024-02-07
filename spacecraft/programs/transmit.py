import random
import time
from typing import Callable, Type, Self

from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.base import BasePart
from spacecraft.parts.manager import PartsManager
from spacecraft.parts.coms_controller import ComsController
from spacecraft.programs.base import BaseProgram, ProgramArgumentParser, ProgramKeyError, ProgramValueError


class TransmitProgram(BaseProgram):
    __PARSER = ProgramArgumentParser(prog="transmit")
    __PARSER.add_argument(
        "coms",
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

    def __assert_controller_type(self, part: BasePart) -> ComsController:
        if not isinstance(part, ComsController):
            raise ProgramValueError(f"{part.part_id} must be a COMS system")
        return part

    def __simulate_wait_time(self, duration: float, max_random_duration: float) -> None:
        # add random duration
        duration += random.uniform(0, max_random_duration)

        # await duration
        self._display.debug("", end="")
        curr_duration: int = 0
        while curr_duration < (duration - 1):  # wait for n seconds
            time.sleep(1)
            self._display.print(".", end="")
            curr_duration += 1

        remaining_duration: float = duration % 1
        time.sleep(remaining_duration)  # wait for the remaining part of a second

        self._display.print("")  # newline

    def __simulate_transmit(self, message: str) -> None:
        self._display.info("transmitting message")
        self.__simulate_wait_time(
            duration=len(message) * self.__TRANSMIT_DURATION_PER_CHAR,
            max_random_duration=self.__TRANSMIT_MAX_RANDOM_DURATION,
        )
        self._display.info("transmission complete")

    def __simulate_response_time(self, message: str) -> None:
        self._display.info("awaiting response")
        self.__simulate_wait_time(
            duration=len(message) * self.__RESPONSE_DURATION_PER_CHAR,
            max_random_duration=self.__RESPONSE_MAX_RANDOM_DURATION,
        )

    def __generate_response(self, coms_controller: ComsController, message: str) -> None:
        self._display.info("receiving response")

        communicator = coms_controller.communicator
        for token in communicator.stream(message):
            self._display.print(token.content, end="")

        self._display.print("")  # newline
        self._display.info("received EOT")

    def exec(self, arguments: list[str]) -> None:
        # transmit 0ab3 "Hello World!"
        arguments = self.__PARSER.parse_args(arguments)
        part_id: str = arguments.coms
        message: str = " ".join(arguments.message)

        # retrieve part
        part = self._get_part_by_id(part_id)
        coms_controller = self.__assert_controller_type(part)

        self.__simulate_transmit(message)
        self.__simulate_response_time(message)
        self.__generate_response(coms_controller, message)
