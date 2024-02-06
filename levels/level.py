from levels.base import Level
from levels.completion import ControllerStatusCompletionChecker, ComsSecretCompletionChecker
from spacecraft.builder import SpacecraftBuilder
from spacecraft.parts.coms_controller import ComsController
from spacecraft.spacecraft import Spacecraft


def adjust_spacecraft_level_0(spacecraft: Spacecraft) -> None:
    ln2_tank = spacecraft.parts_manager.get("de55")
    ln2_tank.power_off()


def adjust_spacecraft_level_1(spacecraft: Spacecraft) -> None:
    main_lox_tank = spacecraft.parts_manager.get("9630")
    main_lox_tank.power_off()
    main_lox_tank.controllable = False


def adjust_spacecraft_level_2(spacecraft: Spacecraft) -> None:
    coms_controller: ComsController = spacecraft.parts_manager.get("1d40")
    coms_controller.secret = "other"


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

level_2_builder = SpacecraftBuilder()
level_2_builder.configured_secret = "somethingelse"
level_2_builder.actual_secret = "cisco"
level_2 = Level(
    name="Level 2",
    prolog="testing prolog",
    epilog="testing epilog",
    completion_checker=ComsSecretCompletionChecker(target_secret="Cisco123"),
    adjust_spacecraft=adjust_spacecraft_level_2,
    init_spacecraft=level_2_builder.build_default,
)

LEVELS: dict[str, Level] = {
    "level-0": level_0,
    "level-1": level_1,
    "level-2": level_2,
}
