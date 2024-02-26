import streamlit as st
from utils import level_utils, shell_utils
from functools import partial
from . import environment as environment_utils

environment_utils.load_env()


def __display_output(content: str, placeholder):
    placeholder.markdown(content)


def __display_narrative(content: str, placeholder):
    for chunk in content.split("\n"):
        placeholder.markdown(f"*{chunk}*")


def init_level_page(level_name: str):
    # page layout
    top = st.container()
    body = st.container()
    bottom = st.container()

    shell_history_container = body.container()
    shell_curr_container = body.container()
    curr_output_placeholder = shell_curr_container.empty()

    # init spacecraft
    level_state = level_utils.init_level(
        level_name,
        display_callback=partial(__display_output, placeholder=curr_output_placeholder)
    )
    spacecraft = level_state.spacecraft
    st.sidebar.write(f"hash: {hash(spacecraft)}")

    # shell history
    shell_history = shell_utils.init_shell_history(level_state.level)
    shell_utils.display_shell_history(shell_history, shell_history_container)

    # fill placeholder
    top.title(level_state.level.name)
    __display_narrative(level_state.level.prolog, top)

    # command input
    command: str = st.chat_input(placeholder="enter your command ...", disabled=level_state.is_complete())
    if command and not level_state.is_complete():
        spacecraft.shell.exec(command)

    # display current output
    output = spacecraft.display.flush()
    __display_output(output, curr_output_placeholder)

    # add output to shell history
    shell_history.append(output)

    # show completion status
    if level_state.is_complete():
        st.sidebar.markdown(f"status: **:green[CRISIS AVERTED]**")

        # show epilog if finished
        __display_narrative(level_state.level.epilog, bottom)
    else:
        st.sidebar.markdown(f"status: **:red[ONGOING CRISIS]**")
