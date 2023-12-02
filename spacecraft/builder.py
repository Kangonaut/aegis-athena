from spacecraft.displays.base import BaseDisplay
from spacecraft.displays.streamlit import StreamlitDisplay
from spacecraft.parts.antenna import Antenna, RangeType, FrequencyRange
from spacecraft.parts.battery import Battery
from spacecraft.parts.cooler import Cooler
from spacecraft.parts.environment_controller import EnvironmentController
from spacecraft.parts.power_controller import PowerController
from spacecraft.parts.fuel import FuelTank, FuelType
from spacecraft.parts.fuel_cell import FuelCell
from spacecraft.parts.temp_controller import TemperatureController
from spacecraft.parts.thermometer import Thermometer
from spacecraft.parts.water import WaterTank
from spacecraft.spacecraft import Spacecraft


class SpacecraftBuilder:
    @staticmethod
    def build_default(display: BaseDisplay) -> Spacecraft:
        spacecraft = Spacecraft(display)

        lox_tank_1 = FuelTank(
            name="LOX tank 1",
            fuel_type=FuelType.LIQUID_OXYGEN,
            content=100,
            capacity=100,
        )
        lh2_tank_1 = FuelTank(
            name="LH2 tank 1",
            fuel_type=FuelType.LIQUID_HYDROGEN,
            content=100,
            capacity=100,
        )
        fuel_cell_1 = FuelCell(name="fuel cell 1")
        fuel_cell_1.oxygen_fuel_tank = lox_tank_1
        fuel_cell_1.hydrogen_fuel_tank = lh2_tank_1

        antenna_1 = Antenna(
            name="short range antenna",
            range_type=RangeType.SHORT_RANGE,
            frequency_range=FrequencyRange(min=2 * 10 ** 9, max=4 * 10 ** 9),
            frequency=3_013_347_988,
        )

        battery_1 = Battery(name="main battery")
        eps_controller = PowerController(
            name="EPS controller",
            battery=battery_1,
            fuel_cell=fuel_cell_1,
        )

        water_tank = WaterTank(
            name="main water tank",
            capacity=100,
            content=100,
            water_supply=fuel_cell_1,
        )

        space_radiator = Cooler(
            name="space radiator",
        )
        interior_thermometer = Thermometer(
            name="interior thermometer"
        )
        interior_temperature_controller = TemperatureController(
            name="interior temperature controller",
            cooler=space_radiator,
            thermometer=interior_thermometer,
        )

        environment_controller = EnvironmentController(
            name="ECS controller",
            temperature_controller=interior_temperature_controller,
            water_tank=water_tank,
        )

        spacecraft.parts_manager.add(lox_tank_1)
        spacecraft.parts_manager.add(lh2_tank_1)
        spacecraft.parts_manager.add(fuel_cell_1)
        spacecraft.parts_manager.add(antenna_1)
        spacecraft.parts_manager.add(battery_1)
        spacecraft.parts_manager.add(eps_controller)
        spacecraft.parts_manager.add(water_tank)
        spacecraft.parts_manager.add(space_radiator)
        spacecraft.parts_manager.add(interior_thermometer)
        spacecraft.parts_manager.add(interior_temperature_controller)
        spacecraft.parts_manager.add(environment_controller)

        return spacecraft
