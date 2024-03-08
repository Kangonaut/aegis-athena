from utils import usage_utils
from usage.base.price_listing import PRICE_LISTINGS

import streamlit as st

st.title("Usage")

store = usage_utils.get_usage_store()

for model in store.models:
    usage = store.aggregate_model_usage(model)
    total_cost = (
            PRICE_LISTINGS[model].input_token_price * usage.num_input_tokens
            + PRICE_LISTINGS[model].output_token_price * usage.num_output_tokens
    )

    container = st.container(border=True)
    container.header(f"{model}")

    container.markdown(f"input tokens: {usage.num_input_tokens}")
    container.markdown(f"output tokens: {usage.num_output_tokens}")

    container.markdown(f"total cost: **${total_cost:.2f}**")
