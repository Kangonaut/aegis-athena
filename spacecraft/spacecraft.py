from spacecraft.displays.base import BaseDisplay
from spacecraft.displays.stdout import StdoutDisplay
from spacecraft.parts.manager import PartsManager
from spacecraft.parts.base import BasePart
from spacecraft.programs.shell import Shell


class Spacecraft:
    def __init__(self, display: BaseDisplay):
        self.parts_manager = PartsManager()
        self.display = display
        self.shell = Shell(self.parts_manager, self.display)
