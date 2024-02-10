import streamlit as st
import weaviate
import os

from llama_index.vector_stores import WeaviateVectorStore


@st.cache_resource()
def get_weaviate_client():
    return weaviate.Client(
        url=os.getenv("WEAVIATE_URL"),
    )


def get_as_vector_store(weaviate_client: weaviate.Client, class_name: str) -> WeaviateVectorStore:
    vector_store = WeaviateVectorStore(
        weaviate_client=weaviate_client,
        index_name=class_name,
        text_key="chunk",
    )
    return vector_store


def is_populated(weaviate_client: weaviate.Client, class_name: str) -> bool:
    if not weaviate_client.schema.exists(class_name):
        return False
    result = weaviate_client.query.aggregate(class_name).with_meta_count().do()
    return result["data"]["Aggregate"][class_name][0]["meta"]["count"] != 0
