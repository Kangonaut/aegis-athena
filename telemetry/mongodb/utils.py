from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

import os
import streamlit as st


@st.cache_resource
def get_client() -> MongoClient:
    return MongoClient(
        host=os.getenv("MONGODB_HOST"),
        port=int(os.getenv("MONGODB_PORT")),
    )


@st.cache_resource
def get_database() -> Database:
    client = get_client()
    return client["aegis-athena-shell-telemetry"]
