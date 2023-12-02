import streamlit as st
from typing import Callable

from spacecraft.builder import SpacecraftBuilder
from spacecraft.displays.streamlit import StreamlitDisplay
from spacecraft.spacecraft import Spacecraft


def init_spacecraft(display_callback: Callable[[str], None]) -> Spacecraft:
    if "spacecraft" not in st.session_state:
        display = StreamlitDisplay(callback=display_callback)
        st.session_state["spacecraft"] = SpacecraftBuilder.build_default(display)
    return st.session_state["spacecraft"]
