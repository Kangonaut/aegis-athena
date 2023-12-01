import streamlit as st
from utils import shell_utils
from test import display, spacecraft

st.title("Aegis Athena")

# layout
shell_container = st.container()

# shell
shell_interactions = shell_utils.init_shell_interactions_memory()
command: str = st.chat_input()
if command:
    spacecraft.shell.exec(command)
    output = display.read_recent()

    # store shell interaction
    interaction = shell_utils.ShellInteraction(command, output)
    shell_interactions.append(interaction)
shell_utils.display_shell_interactions(shell_interactions, shell_container)
