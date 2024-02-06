import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from levels.base import Level


def init_shell_history(level: Level) -> list[str]:
    key: str = f"{level.name}_shell_history"
    if key not in st.session_state:
        st.session_state[key] = []
    return st.session_state[key]


def display_shell_history(shell_history: list[str], display_elem: DeltaGenerator) -> None:
    for output in shell_history:
        display_elem.markdown(output)

        # separate outputs by empty space
        display_elem.markdown("#")
