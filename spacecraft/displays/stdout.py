import builtins

from spacecraft.displays.base import BaseDisplay


class StdoutDisplay(BaseDisplay):
    def print(self, content: str) -> None:
        builtins.print(content)
