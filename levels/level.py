from levels.base import Level
from levels.completion import ControllerStatusCompletionChecker, ComsSecretCompletionChecker
from spacecraft.spacecraft import Spacecraft


def adjust_spacecraft_level_0(spacecraft: Spacecraft) -> None:
    ln2_tank = spacecraft.parts_manager.get("de55")
    ln2_tank.power_off()


def adjust_spacecraft_level_1(spacecraft: Spacecraft) -> None:
    main_lox_tank = spacecraft.parts_manager.get("9630")
    main_lox_tank.power_off()
    main_lox_tank.controllable = False


level_0 = Level(
    name="Level 0 - What the f*ck?",
    prolog="testing prolog",
    epilog="testing epilog",
    completion_checker=ControllerStatusCompletionChecker(),
    adjust_spacecraft=adjust_spacecraft_level_0,
)

level_1 = Level(
    name="Level 1",
    prolog="testing prolog",
    epilog="testing epilog",
    completion_checker=ControllerStatusCompletionChecker(),
    adjust_spacecraft=adjust_spacecraft_level_1,
)

LEVELS: dict[str, Level] = {
    "level-0": level_0,
    "level-1": level_1,
}
