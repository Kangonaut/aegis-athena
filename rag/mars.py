from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import BaseQueryEngine, TransformQueryEngine
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate
from llama_index.core.response_synthesizers import Refine
from llama_index.core.postprocessor import SentenceTransformerRerank, MetadataReplacementPostProcessor
from llama_index.core import VectorStoreIndex
from llama_index.core.query_pipeline import QueryPipeline, InputComponent

import streamlit as st

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


@st.cache_resource()
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


@st.cache_resource()
def get_v5_2(streaming=False) -> BaseQueryEngine:
    """
    Same as v5.1, but uses a different synthesizer for generating the final answer.
    In addition to that, the LLM is configured with :code:`temperature=0.3`, making it a bit more imaginative.

    \\

    v5.2 uses a :code:`Refine` synthesizer with customized prompts.
    The prompts are based on the default prompts, but have an additional line:
    :code:`Please write the answer using simple and clear language.`
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

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3)
    service_context = ServiceContext.from_defaults(llm=llm)

    qa_prompt_tmpl = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query.\n"
        "Please write the answer using simple and clear language.\n"  # custom
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_tmpl)

    refine_prompt_tmpl = (
        "The original query is as follows: {query_str}\n"
        "We have provided an existing answer: {existing_answer}\n"
        "We have the opportunity to refine the existing answer "
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Given the new context, refine the original answer to better "
        "answer the query.\n"
        "Please write the answer using simple and clear language.\n"  # custom
        "If the context isn't useful, return the original answer.\n"
        "Refined Answer: "
    )
    refine_prompt = PromptTemplate(refine_prompt_tmpl)
    response_synthesizer = Refine(
        text_qa_template=qa_prompt,
        refine_template=refine_prompt,
        streaming=True,
    )

    query_engine = index.as_query_engine(
        # hybrid search
        vector_store_query_mode="hybrid",
        alpha=0.75,  # 1 => vector search; 0 => BM25

        service_context=service_context,
        streaming=streaming,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[sentence_window_postprocessor, reranker],
        response_synthesizer=response_synthesizer,
    )

    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    final_query_engine = TransformQueryEngine(query_engine, query_transform=hyde)

    return final_query_engine


def get_v5_2_as_query_pipeline() -> QueryPipeline:
    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 5

    # weaviate
    weaviate_client = weaviate_utils.get_weaviate_client()
    weaviate_vector_store = weaviate_utils.as_vector_store(weaviate_client, weaviate_class_name)
    weaviate_index = VectorStoreIndex.from_vector_store(
        weaviate_vector_store,
    )
    weaviate_retriever = weaviate_index.as_retriever(
        similarity_top_k=similarity_top_k,
        vector_store_query_mode="hybrid",
        alpha=0,  # 1 => vector search; 0 => BM25
    )

    # sentence window retrieval
    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

    # HyDE
    hyde_prompt_template = PromptTemplate(
        "Please write a passage to answer the question\n"
        "Try to include as many key details as possible.\n"
        "\n"
        "{query_str}\n"
        "\n"
        "Passage: "
    )
    hyde_combined_prompt_template = PromptTemplate(
        "Question: {query_str}\n"
        "Answer: {hyde_str}"
    )
    hyde_llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3)

    # Refine response synthesizer
    qa_prompt = PromptTemplate(
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query.\n"
        "Please write the answer using simple and clear language.\n"  # custom
        "Query: {query_str}\n"
        "Answer: "
    )
    refine_prompt = PromptTemplate(
        "The original query is as follows: {query_str}\n"
        "We have provided an existing answer: {existing_answer}\n"
        "We have the opportunity to refine the existing answer "
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Given the new context, refine the original answer to better "
        "answer the query.\n"
        "Please write the answer using simple and clear language.\n"  # custom
        "If the context isn't useful, return the original answer.\n"
        "Refined Answer: "
    )
    response_synthesizer_llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3)
    refine_response_synthesizer = Refine(
        text_qa_template=qa_prompt,
        refine_template=refine_prompt,
        llm=response_synthesizer_llm,
        streaming=True,
    )

    # reranker
    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    # query pipeline
    qp = QueryPipeline()
    qp.add_modules({
        "original_input": InputComponent(),
        "hyde_prompt_template": hyde_prompt_template,
        "hyde_llm": hyde_llm,
        "hyde_combined_prompt_template": hyde_combined_prompt_template,
        "weaviate_retriever": weaviate_retriever,
        "refine_response_synthesizer": refine_response_synthesizer,
        "reranker": reranker,
        "sentence_window_postprocessor": sentence_window_postprocessor,
    })

    # hyde
    qp.add_link("original_input", "hyde_prompt_template", dest_key="query_str")
    qp.add_link("hyde_prompt_template", "hyde_llm")
    qp.add_link("hyde_llm", "hyde_combined_prompt_template", dest_key="hyde_str")
    qp.add_link("original_input", "hyde_combined_prompt_template", dest_key="query_str")
    qp.add_link("hyde_combined_prompt_template", "weaviate_retriever")

    # sentence window retrieval
    qp.add_link("weaviate_retriever", "sentence_window_postprocessor", dest_key="nodes")

    # reranker
    qp.add_link("sentence_window_postprocessor", "reranker", dest_key="nodes")
    qp.add_link("original_input", "reranker", dest_key="query_str")

    # response synthesizer
    qp.add_link("reranker", "refine_response_synthesizer", dest_key="nodes")
    qp.add_link("original_input", "refine_response_synthesizer", dest_key="query_str")
    qp.add_link("original_input", "weaviate_retriever")

    return qp
