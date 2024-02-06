from levels.base import BaseCompletionChecker
from spacecraft.parts.base import PartStatus
from spacecraft.parts.coms_controller import ComsController
from spacecraft.spacecraft import Spacecraft


class ControllerStatusCompletionChecker(BaseCompletionChecker):
    def check_completion(self, spacecraft: Spacecraft) -> bool:
        return all(part.status == PartStatus.NOMINAL for part in spacecraft.parts_manager.get_controllers())


class ComsSecretCompletionChecker(BaseCompletionChecker):
    def __init__(self, target_secret: str):
        self.target_secret = target_secret

    def check_completion(self, spacecraft: Spacecraft) -> bool:
        coms_controller: ComsController = spacecraft.parts_manager.get("1d40")
        return coms_controller.secret == self.target_secret
