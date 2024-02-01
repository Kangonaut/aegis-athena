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
from spacecraft.parts.engine import Engine
from spacecraft.parts.gimbal import EngineGimbal
from spacecraft.parts.sps_controller import SpsController
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
        aerozine_tank = AerozineTank(
            name="Aerozine 50 tank",
            capacity=1_000,
            fill_level=900,
        )
        n2o4_tank = N2o4Tank(
            name="N2O4 tank",
            capacity=1_000,
            fill_level=900,
        )
        engine = Engine(
            name="Aerojet AJ10",
            fuel_tank=aerozine_tank,
            oxidizer_tank=n2o4_tank,
        )
        gimbal = EngineGimbal(
            name="TVC gimbal"
        )
        sps_controller = SpsController(
            name="SPS controller",
            engine=engine,
            gimbal=gimbal,
        )
        spacecraft.parts_manager.add_many([
            aerozine_tank,
            n2o4_tank,
            engine,
            gimbal,
            sps_controller,
        ])

        # COMS
        main_short_range_antenna = Antenna(
            name="VHF scimitar antenna 0",
            range_type=RangeType.SHORT_RANGE,
            frequency=296_800_000,  # or 259_700_000
            frequency_range=FrequencyRange(30_000_000, 300_000_000),
        )
        backup_short_range_antenna = Antenna(
            name="VHF scimitar antenna 1",
            range_type=RangeType.SHORT_RANGE,
            frequency=296_800_000,  # or 259_700_000
            frequency_range=FrequencyRange(30_000_000, 300_000_000),
        )
        main_long_range_antenna = Antenna(
            name="USB antenna",
            range_type=RangeType.LONG_RANGE,
            frequency=2_119_000_000_000,
            frequency_range=FrequencyRange(2_025_000_000, 2_290_000_000),
        )
        coms_controller = ComsController(
            name="COMS controller",
            antenna=main_short_range_antenna,
            secret="cisco",  # configured secret
            dispatcher=DefaultCommunicationDispatcher(
                secret="class",  # actual secret
            ),
        )
        spacecraft.parts_manager.add_many([
            main_short_range_antenna,
            backup_short_range_antenna,
            main_long_range_antenna,
            coms_controller,
        ])

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
