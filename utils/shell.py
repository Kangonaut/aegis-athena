import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def init_shell_history() -> list[str]:
    if "shell_history" not in st.session_state:
        st.session_state["shell_history"] = []
    return st.session_state["shell_history"]


def display_shell_history(shell_history: list[str], display_elem: DeltaGenerator) -> None:
    for output in shell_history:
        display_elem.markdown(output)

        # separate outputs by empty space
        display_elem.markdown("#")
