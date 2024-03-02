from utils import telemetry_utils
import streamlit as st

st.title("Traces")

manager = telemetry_utils.get_telemetry_manager()
trace_ids: list[str] = manager.get_all_trace_ids()

trace_id = st.selectbox(
    label="Select a Trace:",
    options=trace_ids,
)

trace = manager.get(trace_id)
for node in trace.nodes:
    timestamp_str: str = node.timestamp.strftime("%Y.%m.%d %H:%M:%S")

    st.markdown(f"**timestamp:** {timestamp_str}")
    container = st.container(border=True)
    container.markdown(node.content)
    st.divider()
