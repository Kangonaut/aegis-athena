import streamlit as st

from llama_index.core import VectorStoreIndex, StorageContext, ServiceContext
from llama_index.core.chat_engine import ContextChatEngine, CondensePlusContextChatEngine
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.cohere_rerank import CohereRerank

from agent.knowledge_base.retriever.mars import MarsKnowledgeBaseRetriever
from rag import weaviate_utils, mongodb_utils

# HyDE
HYDE_LLM_TEMPERATURE: float = 0.2
HYDE_LLM_MODEL: str = "gpt-3.5-turbo-0125"

# similarity search
WEAVIATE_CLASS_NAME: str = "AutoMergingDocsChunk"
RETRIEVER_HYBRID_SEARCH_ALPHA: float = 0.85  # 1 => vector search; 0 => BM25
RETRIEVER_SIMILARITY_TOP_K: int = 15

# auto-merging retrieval
AUTO_MERGING_RATION_THRESHOLD: float = 0.2

# reranking
RERANK_TOP_N: int = 3
RERANK_MODEL: str = "rerank-english-v2.0"


@st.cache_resource
def get_knowledge_base_retriever():
    # HyDE
    hyde_llm = OpenAI(
        model=HYDE_LLM_MODEL,
        temperature=HYDE_LLM_TEMPERATURE,
    )

    # Weaviate
    weaviate_client = weaviate_utils.get_weaviate_client()
    weaviate_vector_store = weaviate_utils.as_vector_store(weaviate_client, WEAVIATE_CLASS_NAME)
    weaviate_index = VectorStoreIndex.from_vector_store(weaviate_vector_store)
    weaviate_retriever = weaviate_index.as_retriever(
        similarity_top_k=RETRIEVER_SIMILARITY_TOP_K,
        vector_store_query_mode="hybrid",
        alpha=RETRIEVER_HYBRID_SEARCH_ALPHA,
    )

    # MongoDB
    mongodb_client = mongodb_utils.get_client()
    mongodb_docstore = mongodb_utils.as_docstore(mongodb_client)
    mongodb_storage_context = StorageContext.from_defaults(docstore=mongodb_docstore)

    # auto-merging retriever
    auto_merging_retriever = AutoMergingRetriever(
        simple_ratio_thresh=AUTO_MERGING_RATION_THRESHOLD,
        vector_retriever=weaviate_retriever,
        storage_context=mongodb_storage_context,
        verbose=True,
    )

    # reranker
    reranker = CohereRerank(
        top_n=RERANK_TOP_N,
        model=RERANK_MODEL,
    )

    return MarsKnowledgeBaseRetriever.from_defaults(
        hyde_llm=hyde_llm,
        reranker=reranker,
        retriever=auto_merging_retriever,
    )


CHAT_ENGINE_SYSTEM_PROMPT = """\
You are an AI assistant called MARS that is designed to help the astronaut crew on the Aegis Athena spaceflight mission.
You are currently talking to the astronaut Wade, who is currently in the SPACECRAFT module.
Wade can only interact with the SPACECRAFT module via the ship's console.
"""
CHAT_ENGINE_CONTEXT_PROMPT = (
    "Context information is below."
    "\n--------------------\n"
    "{context_str}"
    "\n--------------------\n"
    "Given the context information and not prior knowledge, answer the user's query.\n"
)

CHAT_ENGINE_LLM_MODEL = "gpt-3.5-turbo"
CHAT_ENGINE_LLM_TEMPERATURE = 0.1


def build_chat_engine() -> BaseChatEngine:
    knowledge_base_retriever = get_knowledge_base_retriever()
    llm = OpenAI(model=CHAT_ENGINE_LLM_MODEL, temperature=CHAT_ENGINE_LLM_TEMPERATURE)
    service_context = ServiceContext.from_defaults(
        llm=llm
    )
    # chat_engine = ContextChatEngine.from_defaults(
    #     retriever=knowledge_base_retriever,
    #     service_context=service_context,
    #     system_prompt=CHAT_ENGINE_SYSTEM_PROMPT,
    #     context_template=CHAT_ENGINE_CONTEXT_TEMPLATE,
    # )
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        retriever=knowledge_base_retriever,
        llm=llm,
        system_prompt=CHAT_ENGINE_SYSTEM_PROMPT,
        # context_prompt=CHAT_ENGINE_CONTEXT_PROMPT,
        verbose=True,
    )
    return chat_engine
