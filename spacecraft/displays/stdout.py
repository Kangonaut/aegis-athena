import builtins

from spacecraft.displays.base import BaseDisplay


class StdoutDisplay(BaseDisplay):
    def print(self, string: str) -> None:
        builtins.print(string)
