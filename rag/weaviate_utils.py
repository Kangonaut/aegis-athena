import streamlit as st
import weaviate
import os


@st.cache_resource()
def get_weaviate_client():
    return weaviate.Client(
        url=os.getenv("WEAVIATE_URL"),
    )
