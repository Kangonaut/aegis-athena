from llama_index.query_engine import BaseQueryEngine
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI

import streamlit as st
from llama_index.vector_stores import WeaviateVectorStore

from rag import weaviate_utils


@st.cache_resource()
def get_v1(streaming=False) -> BaseQueryEngine:
    """
    Simple RAG setup with Weaviate as vector database (:code:`class_name="DocsChunk"`).
    The Synthesizer uses the :code:`gpt-3.5-turbo` (:code:`temperature=0.1`) model.
    """

    weaviate_class_name: str = "MarkdownDocsChunk"

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(service_context=service_context, streaming=streaming)

    return query_engine
