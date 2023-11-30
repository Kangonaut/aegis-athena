from typing import Self, Type, Callable
import abc
import argparse
import io


class BaseTerminal(abc.ABC):
    def execute(self, command: list[str], out_stream: io.StringIO) -> None:
        subcommand: str = command[0]

        if subcommand in self._TERMINAL_MAPPING:
            sub_terminal: BaseTerminal = self._TERMINAL_MAPPING[subcommand]()
            sub_terminal.execute(command[1:], out_stream)
        elif subcommand in self._COMMAND_MAPPING:
            self._COMMAND_MAPPING[subcommand](command[1:])

    _TERMINAL_MAPPING: dict[str, Type[Self]] = {}
    _COMMAND_MAPPING: dict[str, Callable[[list[str]], None]] = {}
