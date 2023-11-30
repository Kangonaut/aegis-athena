import streamlit as st
import io

from parts.fuel import FuelTank, FuelType
from parts.fuel_cell import FuelCell
from terminal.root import RootTerminal


@st.cache_resource
def get_terminal():
    lox_tank_1 = FuelTank(
        name="LOX tank 1",
        fuel_type=FuelType.LIQUID_OXYGEN,
        fuel_content=100,
        fuel_capacity=100,
    )
    lh2_tank_1 = FuelTank(
        name="LH2 tank 1",
        fuel_type=FuelType.LIQUID_HYDROGEN,
        fuel_content=100,
        fuel_capacity=100,
    )
    fuel_cell_1 = FuelCell(name="fuel cell 1")

    fuel_cell_1.oxygen_fuel_tank = lox_tank_1
    fuel_cell_1.hydrogen_fuel_tank = lh2_tank_1

    return RootTerminal()


st.title("Aegis Athena")

st.markdown("This is an [ **:red[ERROR]** ].")

terminal = get_terminal()

out_stream = io.StringIO()

terminal.execute_raw(f"part list", out_stream)


with st.chat_message(name="ai"):
    output = out_stream.getvalue()
    print(output)
    st.markdown(output)
