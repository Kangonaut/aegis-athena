from spacecraft.communication.dispatcher import DefaultCommunicationDispatcher
from spacecraft.displays.base import BaseDisplay
from spacecraft.parts.ars import Fan, HeatExchanger, WaterSeparator, OdorRemover, Co2Remover, ArsController
from spacecraft.parts.coms import Antenna, RangeType, FrequencyRange
from spacecraft.parts.coms_controller import ComsController
from spacecraft.parts.ecs import EcsController
from spacecraft.parts.eps import Battery, FuelCell, EpsController
from spacecraft.parts.brains import BrainsController, GraphicsProcessingUnit, StorageArray, StorageMedium
from spacecraft.parts.fuel import LoxTank, Lh2Tank, AerozineTank, N2o4Tank, Ln2Tank
from spacecraft.parts.hts import CoolingLoop, Radiator, CoolantPump, Thermometer, HtsController
from spacecraft.parts.oscpcs import OscpcsController
from spacecraft.parts.sps import Engine, EngineGimbal, SpsController
from spacecraft.parts.wcs import WaterTank, WaterPump, WcsController
from spacecraft.spacecraft import Spacecraft


class SpacecraftBuilder:
    def __init__(self):
        self.configured_secret: str = "cisco"
        self.actual_secret: str = "cisco"

    def build_default(self, display: BaseDisplay) -> Spacecraft:
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
            secret=self.configured_secret,  # configured secret
            dispatcher=DefaultCommunicationDispatcher(
                secret=self.actual_secret,  # actual secret
            ),
        )
        spacecraft.parts_manager.add_many([
            main_short_range_antenna,
            backup_short_range_antenna,
            main_long_range_antenna,
            coms_controller,
        ])

        # BRAINS
        gpu_0 = GraphicsProcessingUnit(name="GPU 0")
        gpu_1 = GraphicsProcessingUnit(name="GPU 1")
        gpu_2 = GraphicsProcessingUnit(name="GPU 2")
        gpu_3 = GraphicsProcessingUnit(name="GPU 3")
        gpu_4 = GraphicsProcessingUnit(name="GPU 4")
        gpu_5 = GraphicsProcessingUnit(name="GPU 5")
        gpu_6 = GraphicsProcessingUnit(name="GPU 6")
        gpu_7 = GraphicsProcessingUnit(name="GPU 7")
        gpu_8 = GraphicsProcessingUnit(name="GPU 8")
        gpu_9 = GraphicsProcessingUnit(name="GPU 9")

        disk_0 = StorageMedium(
            name="SSD 0",
            capacity=5_000_000_000,
        )
        disk_1 = StorageMedium(
            name="SSD 1",
            capacity=5_000_000_000,
        )
        disk_2 = StorageMedium(
            name="SSD 2",
            capacity=5_000_000_000,
        )
        disk_3 = StorageMedium(
            name="SSD 3",
            capacity=5_000_000_000,
        )
        disk_array = StorageArray(
            name="RAID 5 array",
            storage_elems=[disk_0, disk_1, disk_2, disk_3]
        )

        brains_controller = BrainsController(
            name="BRAINS Controller",
            storage=disk_array,
            gpus=[gpu_0, gpu_1, gpu_2, gpu_3, gpu_4, gpu_5, gpu_6, gpu_7, gpu_8, gpu_9]
        )

        spacecraft.parts_manager.add_many([
            gpu_0, gpu_1, gpu_2, gpu_3, gpu_4, gpu_5, gpu_6, gpu_7, gpu_8, gpu_9,
            disk_0, disk_1, disk_2, disk_3,
            disk_array,
            brains_controller,
        ])

        # ECS - WMS
        main_water_tank = WaterTank(
            name="H2O tank 0",
            capacity=100,
            fill_level=60,
            water_supply=main_fuel_cell,
        )
        backup_water_tank = WaterTank(
            name="H2O tank 1",
            capacity=100,
            fill_level=100,
            water_supply=main_fuel_cell,
        )
        main_water_pump = WaterPump(
            name="H2O pump 0",
            water_tank=main_water_tank,
        )
        backup_water_pump = WaterPump(
            name="H2O pump 1",
            water_tank=main_water_tank,
        )
        wcs_controller = WcsController(
            name="WCS controller",
            water_pump=main_water_pump,
        )

        spacecraft.parts_manager.add_many([
            main_water_tank,
            backup_water_tank,
            main_water_pump,
            backup_water_pump,
            wcs_controller,
        ])

        # ECS - HTS
        main_coolant_pump = CoolantPump(
            name="coolant pump 0",
        )
        backup_coolant_pump = CoolantPump(
            name="coolant pump 1",
        )
        main_space_radiator = Radiator(
            name="space radiator 0",
        )
        backup_space_radiator = Radiator(
            name="space radiator 1"
        )
        main_cooling_loop = CoolingLoop(
            name="cooling loop 0",
            radiator=main_space_radiator,
            coolant_pump=main_coolant_pump,
        )
        backup_cooling_loop = CoolingLoop(
            name="cooling loop 1",
            radiator=main_space_radiator,
            coolant_pump=main_coolant_pump,
        )
        main_cabin_thermometer = Thermometer(
            name="cabin thermometer 0",
        )
        backup_cabin_thermometer = Thermometer(
            name="cabin thermometer 1",
        )
        hts_controller = HtsController(
            name="HTS controller",
            cooling_loop=main_cooling_loop,
            thermometer=main_cabin_thermometer,
        )
        spacecraft.parts_manager.add_many([
            main_coolant_pump,
            backup_coolant_pump,
            main_space_radiator,
            backup_space_radiator,
            main_cooling_loop,
            backup_cooling_loop,
            main_cabin_thermometer,
            backup_cabin_thermometer,
            hts_controller,
        ])

        # ECS - ARS
        main_fan = Fan(
            name="fan 0",
        )
        backup_fan = Fan(
            name="fan 1",
        )
        heat_exchanger = HeatExchanger(
            name="heat exchanger",
            cooling_loop=main_cooling_loop,
        )
        main_water_seperator = WaterSeparator(
            name="centrifugal seperator 0",
        )
        backup_water_seperator = WaterSeparator(
            name="centrifugal seperator 1",
        )
        main_odor_remover = OdorRemover(
            name="activated charcoal canister 0",
        )
        backup_odor_remover = OdorRemover(
            name="activated charcoal canister 1",
        )
        main_co2_remover = Co2Remover(
            name="LiOH canister 0",
        )
        backup_co2_remover = Co2Remover(
            name="LiOH canister 1",
        )
        ars_controller = ArsController(
            name="ARS controller",
            fan=main_fan,
            heat_exchanger=heat_exchanger,
            water_separator=main_water_seperator,
            odor_remover=main_odor_remover,
            co2_remover=main_co2_remover,
        )
        spacecraft.parts_manager.add_many([
            main_fan,
            backup_fan,
            heat_exchanger,
            main_water_seperator,
            backup_water_seperator,
            main_odor_remover,
            backup_odor_remover,
            main_co2_remover,
            backup_co2_remover,
            ars_controller,
        ])

        # ECS - OSCPCS
        ln2_tank = Ln2Tank(
            name="LN2 tank",
            capacity=100,
            fill_level=100,
        )
        oscpcs_controller = OscpcsController(
            name="OSCPCS controller",
            lox_tank=main_lox_tank,
            ln2_tank=ln2_tank,
        )
        spacecraft.parts_manager.add_many([
            ln2_tank,
            oscpcs_controller,
        ])

        # ECS
        ecs_controller = EcsController(
            name="ECS controller",
            wcs_controller=wcs_controller,
            ars_controller=ars_controller,
            oscpcs_controller=oscpcs_controller,
            hts_controller=hts_controller,
        )
        spacecraft.parts_manager.add(ecs_controller)

        return spacecraft
