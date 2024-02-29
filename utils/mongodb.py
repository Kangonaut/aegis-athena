import streamlit as st
from pymongo import MongoClient
import os

MONGODB_HOST_ENV_VAR: str = "MONGODB_HOST"
MONGODB_PORT_ENV_VAR: str = "MONGODB_PORT"


@st.cache_resource
def get_client(
        host: str | None = None,
        port: int | None = None,
) -> MongoClient:
    return MongoClient(
        host=host or os.getenv(MONGODB_HOST_ENV_VAR),
        port=port or int(os.getenv(MONGODB_PORT_ENV_VAR)),
    )
