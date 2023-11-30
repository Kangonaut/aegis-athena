import io

from .base import BaseTerminal
from .part import PartTerminal


class RootTerminal(BaseTerminal):
    _TERMINAL_MAPPING = {
        "part": PartTerminal,
    }

    def execute_raw(self, raw_command: str, out_stream: io.StringIO) -> None:
        command: list[str] = raw_command.split()

        try:
            self.execute(command, out_stream)
        except Exception as ex:
            print(ex, file=out_stream)
