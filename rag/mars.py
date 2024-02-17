from llama_index.indices.query.query_transform import HyDEQueryTransform
from llama_index.query_engine import BaseQueryEngine, TransformQueryEngine
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI, Ollama
from llama_index.postprocessor import SentenceTransformerRerank, MetadataReplacementPostProcessor

import streamlit as st
from llama_index.vector_stores import WeaviateVectorStore

from rag import weaviate_utils


@st.cache_resource()
def get_v1_0(streaming=False) -> BaseQueryEngine:
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


@st.cache_resource()
def get_v1_1(streaming=False) -> BaseQueryEngine:
    """
    Same setup as v1.0, but utilizing the `gpt-4` model.
    """

    weaviate_class_name: str = "MarkdownDocsChunk"

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    llm = OpenAI(model="gpt-4", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(service_context=service_context, streaming=streaming)

    return query_engine


@st.cache_resource()
def get_v1_2(streaming=False) -> BaseQueryEngine:
    """
    Same setup as v1.0, but using a BGE reranker, to rerank the retrieved nodes.
    """

    weaviate_class_name: str = "MarkdownDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)
    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[reranker]
    )

    return query_engine


@st.cache_resource()
def get_v2_0(streaming=False) -> BaseQueryEngine:
    """
    Uses sentence window retrieval (:code:`class_name="SentenceWindowDocsChunk"`),
    in order to provide more context and allow for more precise retrieval.
    Like v1.2 it also uses a bi-encoder based re-ranker after the retrieval stage.
    """

    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    return query_engine


@st.cache_resource()
def get_v3_0(streaming=False) -> BaseQueryEngine:
    """
    Same as v2.0, but with HyDE query transformation.
    HyDE hallucinates a hypothetical answer to the query, which is then used for retrieving similar nodes.
    """

    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine


@st.cache_resource()
def get_v4_0(streaming=False) -> BaseQueryEngine:
    """
    Same as v3.0, but using the Llama-2-7b-chat-hf (:code:`llama2:7b`) model run on a local Ollama server instance.
    """

    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = Ollama(model="llama2:7b", request_timeout=600.0, temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine


@st.cache_resource()
def get_v4_1(streaming=False) -> BaseQueryEngine:
    """
    Same as v3.0, but using the phi-2 (:code:`phi:2.7b`) model run on a local Ollama server instance.
    """

    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = Ollama(model="phi:2.7b", request_timeout=600.0, temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine


@st.cache_resource()
def get_v4_2(streaming=False) -> BaseQueryEngine:
    """
    Same as v3.0, but using the TinyLlama-1.1B-Chat-v1.0 (:code:`tinyllama:1.1b`) model run on a local Ollama server instance.
    """

    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = Ollama(model="tinyllama:1.1b", request_timeout=600.0, temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine


@st.cache_resource()
def get_v5_0(streaming=False) -> BaseQueryEngine:
    """
    Same as v3.0, but with hybrid vector search.
    Hybrid search combines dense (similarity based) search with sparse (keyword based) search using the BM25F algorithm.

    configuration: :code:`alpha = 0.75` (1 => pure vector search; 0 => pure BM25)
    """

    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        # hybrid search
        vector_store_query_mode="hybrid",
        alpha=0.75,  # 1 => vector search; 0 => BM25

        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine


st.cache_resource()


def get_v5_1(streaming=False) -> BaseQueryEngine:
    """
    Same as v5.0, but using a larger sentence window.

    v5.0 uses a sentence window of :code:`window_size=3`.

    v5.1 uses a sentence window of :code:`window_size=5`.
    """

    weaviate_class_name: str = "LargerSentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 3

    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    index = VectorStoreIndex.from_vector_store(vector_store)

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine = index.as_query_engine(
        # hybrid search
        vector_store_query_mode="hybrid",
        alpha=0.75,  # 1 => vector search; 0 => BM25

        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker]
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine
