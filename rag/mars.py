from llama_index.query_engine import BaseQueryEngine
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI

import streamlit as st

from rag import weaviate_utils

CLASS_NAME: str = "DocsChunk"


@st.cache_resource()
def get_v1() -> BaseQueryEngine:
    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, CLASS_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store)

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(service_context=service_context, streaming=True)

    return query_engine
