from utils import usage_utils

import streamlit as st

st.title("Usage")

store = usage_utils.get_usage_store()

for model in store.models:
    usage = store.aggregate_model_usage(model)

    container = st.container(border=True)
    container.header(f"{model}")

    container.markdown(f"input tokens: {usage.num_input_tokens}")
    container.markdown(f"output tokens: {usage.num_output_tokens}")
