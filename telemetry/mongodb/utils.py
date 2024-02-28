from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

import os
import streamlit as st

DEFAULT_DB_NAME: str = "aegis-athena-telemetry"


@st.cache_resource
def get_client() -> MongoClient:
    return MongoClient(
        host=os.getenv("MONGODB_HOST"),
        port=int(os.getenv("MONGODB_PORT")),
    )


@st.cache_resource
def get_database(db_name: str = DEFAULT_DB_NAME) -> Database:
    client = get_client()
    return client[db_name]
