from levels.base import Level
from telemetry.base import BaseShellTrace, BaseShellTelemetryManager
from telemetry.mongodb.manager import MongoDbShellTelemetryManager

import streamlit as st
import uuid


@st.cache_resource
def get_telemetry_manager() -> BaseShellTelemetryManager:
    return MongoDbShellTelemetryManager.from_defaults()


def init_shell_trace(level: Level) -> BaseShellTrace:
    telemetry_manager = get_telemetry_manager()
    key: str = f"{level.name}_shell_trace_id"

    # check if trace exists
    if key not in st.session_state:
        # new trace
        trace_id: str = str(uuid.uuid4())
        st.session_state[key] = trace_id
        trace = telemetry_manager.create(trace_id)
    else:
        # existing trace
        trace_id: str = st.session_state[key]
        trace = telemetry_manager.get(trace_id)

    return trace
