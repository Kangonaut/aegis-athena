from spacecraft.communication.dispatcher import DefaultCommunicationDispatcher
from spacecraft.displays.base import BaseDisplay
from spacecraft.displays.streamlit import StreamlitDisplay
from spacecraft.parts.antenna import Antenna, RangeType, FrequencyRange
from spacecraft.parts.battery import Battery
from spacecraft.parts.coms_controller import ComsController
from spacecraft.parts.cooler import Cooler
from spacecraft.parts.environment_controller import EnvironmentController
from spacecraft.parts.eps_controller import EpsController
from spacecraft.parts.fuel import LoxTank, Lh2Tank, AerozineTank, N2o4Tank
from spacecraft.parts.fuel_cell import FuelCell
from spacecraft.parts.temp_controller import TemperatureController
from spacecraft.parts.thermometer import Thermometer
from spacecraft.parts.water import WaterTank
from spacecraft.spacecraft import Spacecraft


class SpacecraftBuilder:
    @staticmethod
    def build_default(display: BaseDisplay) -> Spacecraft:
        spacecraft = Spacecraft(display)

        # EPS
        main_battery = Battery(
            name="battery 0"
        )
        backup_battery = Battery(
            name="battery 1"
        )
        main_lox_tank = LoxTank(
            name="LOX tank 0",
            fill_level=100,
            capacity=100,
        )
        backup_lox_tank = LoxTank(
            name="LOX tank 1",
            fill_level=100,
            capacity=100,
        )
        main_lh2_tank = Lh2Tank(
            name="LH2 tank 0",
            fill_level=100,
            capacity=100,
        )
        backup_lh2_tank = Lh2Tank(
            name="LH2 tank 1",
            fill_level=100,
            capacity=100,
        )
        main_fuel_cell = FuelCell(
            name="fuel cell 0",
            lox_tank=main_lox_tank,
            lh2_tank=main_lh2_tank,
        )
        backup_fuel_cell = FuelCell(
            name="fuel cell 1",
            lox_tank=main_lox_tank,
            lh2_tank=main_lh2_tank,
        )
        eps_controller = EpsController(
            name="EPS controller",
            battery=main_battery,
            fuel_cell=main_fuel_cell,
        )

        spacecraft.parts_manager.add_many([
            main_battery,
            backup_battery,
            main_lox_tank,
            backup_lox_tank,
            main_lh2_tank,
            backup_lh2_tank,
            main_fuel_cell,
            backup_fuel_cell,
            eps_controller,
        ])

        # SPS

        # COMS
        main_low_range_antenna = Antenna(
            name="short-range antenna",
            range_type=RangeType.SHORT_RANGE,
            frequency=1_000,
            frequency_range=FrequencyRange(500, 2_000),
        )
        spacecraft.parts_manager.add(main_low_range_antenna)

        # antenna_1 = Antenna(
        #     name="short range antenna",
        #     range_type=RangeType.SHORT_RANGE,
        #     frequency_range=FrequencyRange(min=2 * 10 ** 9, max=4 * 10 ** 9),
        #     frequency=3_013_347_988,
        # )
        #
        # battery_1 = Battery(name="main battery")
        # eps_controller = EpsController(
        #     name="EPS controller",
        #     battery=battery_1,
        #     fuel_cell=fuel_cell_1,
        # )
        #
        # water_tank = WaterTank(
        #     name="main water tank",
        #     capacity=100,
        #     content=100,
        #     water_supply=fuel_cell_1,
        # )
        #
        # space_radiator = Cooler(
        #     name="space radiator",
        # )
        # interior_thermometer = Thermometer(
        #     name="interior thermometer"
        # )
        # interior_temperature_controller = TemperatureController(
        #     name="interior temperature controller",
        #     cooler=space_radiator,
        #     thermometer=interior_thermometer,
        # )
        #
        # environment_controller = EnvironmentController(
        #     name="ECS controller",
        #     temperature_controller=interior_temperature_controller,
        #     water_tank=water_tank,
        # )
        #
        # communication_controller = CommunicationController(
        #     name="COMS controller",
        #     secret="cisco",  # configured secret
        #     antenna=antenna_1,
        #     dispatcher=DefaultCommunicationDispatcher(
        #         secret="class",  # actual secret
        #     ),
        # )

        return spacecraft
