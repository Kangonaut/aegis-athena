from levels.base import BaseCompletionChecker
from spacecraft.parts.base import PartStatus
from spacecraft.spacecraft import Spacecraft


class ControllerStatusCompletionChecker(BaseCompletionChecker):
    def check_completion(self, spacecraft: Spacecraft) -> bool:
        return all(part.status == PartStatus.NOMINAL for part in spacecraft.parts_manager.get_controllers())
