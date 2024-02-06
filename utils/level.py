import streamlit as st
from typing import Callable, Type
from levels.level import LEVELS
from levels.base import Level, LevelState
from spacecraft.displays.streamlit import StreamlitDisplay


def init_level(level_name: str, display_callback: Callable[[str], None]) -> LevelState:
    if level_name not in st.session_state:
        display = StreamlitDisplay(callback=display_callback)
        st.session_state[level_name] = LEVELS[level_name].init_level_state(display)
    return st.session_state[level_name]
