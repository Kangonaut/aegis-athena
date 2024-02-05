import streamlit as st
from typing import Callable, Type

from levels.level import Level, Level0
from spacecraft.displays.streamlit import StreamlitDisplay

LEVELS: dict[str, Type[Level]] = {
    "level-0": Level0,
}


def init_level(level_name: str, display_callback: Callable[[str], None]) -> Level:
    if level_name not in st.session_state:
        display = StreamlitDisplay(callback=display_callback)
        st.session_state[level_name] = LEVELS[level_name](display)
    return st.session_state[level_name]
