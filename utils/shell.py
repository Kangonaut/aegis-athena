import streamlit as st
from streamlit.delta_generator import DeltaGenerator


class ShellInteraction:
    def __init__(self, command: str, output: str):
        self.command = command
        self.output = output

    def display(self, display_elem: DeltaGenerator):
        display_elem.markdown(f"**:violet[system]:/ $ {self.command}**")
        display_elem.markdown(self.output)


def init_shell_interactions_memory() -> list[ShellInteraction]:
    if "shell_interactions" not in st.session_state:
        st.session_state["shell_interactions"] = []
    return st.session_state["shell_interactions"]


def display_shell_interactions(shell_interactions: list[ShellInteraction], display_elem: DeltaGenerator) -> None:
    for interaction in shell_interactions:
        interaction.display(display_elem)
