import streamlit as st

from utils import shell_utils, spacecraft_utils


def display_curr_output(content: str):
    curr_output_placeholder.markdown(content)


# init spacecraft
spacecraft = spacecraft_utils.init_spacecraft(
    display_callback=display_curr_output
)

# page layout
st.title(f"Aegis Athena {hash(spacecraft)}")
shell_history_container = st.container()
shell_curr_container = st.container()
curr_output_placeholder = shell_curr_container.empty()

# shell history
shell_history = shell_utils.init_shell_history()
shell_utils.display_shell_history(shell_history, shell_history_container)

# command input
shell_interactions = shell_utils.init_shell_history()
command: str = st.chat_input()
if command:
    spacecraft.shell.exec(command)

    # display current output
    output = spacecraft.display.flush()
    display_curr_output(output)

    # add output to shell history
    shell_history.append(output)
