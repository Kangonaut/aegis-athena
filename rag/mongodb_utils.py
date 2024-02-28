from pymongo import MongoClient
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.docstore.mongodb.base import MongoDBKVStore

import os
import streamlit as st

DEFAULT_DB_NAME: str = "aegis-athena-data"


@st.cache_resource
def get_client() -> MongoClient:
    return MongoClient(
        host=os.getenv("MONGODB_HOST"),
        port=int(os.getenv("MONGODB_PORT")),
    )


def as_docstore(client: MongoClient, db_name: str = DEFAULT_DB_NAME) -> MongoDocumentStore:
    return MongoDocumentStore(
        mongo_kvstore=MongoDBKVStore(
            mongo_client=client,
            db_name=db_name,
        ),
    )
