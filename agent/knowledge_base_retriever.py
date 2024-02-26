import streamlit as st
from abc import ABC, abstractmethod

from llama_index.core import VectorStoreIndex, PromptTemplate
from llama_index.core.postprocessor import MetadataReplacementPostProcessor, SentenceTransformerRerank
from llama_index.core.query_pipeline import InputComponent, QueryPipeline
from llama_index.core.schema import NodeWithScore
from llama_index.llms.openai import OpenAI

from rag import weaviate_utils


class BaseKnowledgeBaseExtractFormatter(ABC):
    @abstractmethod
    def format(self, nodes: list[NodeWithScore]) -> str:
        pass


class SimpleKnowledgeBaseExtractFormatter(BaseKnowledgeBaseExtractFormatter):
    def format(self, nodes: list[NodeWithScore]) -> str:
        output: str = (
            "Extracts from the Aegis Athena mission documentation:\n"
        )
        for idx, node in enumerate(nodes):
            output += (
                f"\nSTART OF EXTRACT #{idx + 1}\n"
                f"{node.text}"
                f"\nEND OF EXTRACT #{idx + 1}\n"
            )
        return output


class BaseKnowledgeBaseRetriever(ABC):
    def __init__(
            self,
            formatter: BaseKnowledgeBaseExtractFormatter
    ) -> None:
        self.formatter = formatter

    @abstractmethod
    def retrieve_raw(self, query: str) -> list[NodeWithScore]:
        """
        Retrieve relevant extracts from the knowledge base.

        :param query: in form of a question
        :return: retrieved nodes
        """

    def retrieve_formatted(self, query: str) -> str:
        """
        Retrieve relevant extracts from the knowledge base as a formatted string.

        :param query: in form of a question
        :return: retrieved extracts combined into formatted string.
        """
        nodes = self.retrieve_raw(query)
        return self.formatter.format(nodes)


class QueryPipelineKnowledgeBaseRetriever(BaseKnowledgeBaseRetriever):
    def __init__(
            self,
            query_pipeline: QueryPipeline,
            formatter: BaseKnowledgeBaseExtractFormatter,
    ) -> None:
        super().__init__(formatter)
        self.query_pipeline = query_pipeline

    @classmethod
    def from_defaults(
            cls,
            query_pipeline: QueryPipeline,
            formatter: BaseKnowledgeBaseExtractFormatter | None = None
    ) -> "QueryPipelineKnowledgeBaseRetriever":
        return cls(
            query_pipeline=query_pipeline,
            formatter=formatter or SimpleKnowledgeBaseExtractFormatter(),
        )

    def retrieve_raw(self, query: str) -> str:
        return self.query_pipeline.run(input=query)


# similarity search
WEAVIATE_CLASS_NAME: str = "SentenceWindowDocsChunk"
HYBRID_SEARCH_ALPHA: float = 0.75  # 1 => vector search; 0 => BM25
SIMILARITY_TOP_K: int = 6

# reranking
RERANKER_MODEL: str = "BAAI/bge-reranker-base"
RERANKED_TOP_N: int = 3

# HyDE
HYDE_LLM_TEMPERATURE: float = 0.2
HYDE_LLM_MODEL: str = "gpt-3.5-turbo"


@st.cache_resource
def get_knowledge_base_retriever():
    # weaviate
    weaviate_client = weaviate_utils.get_weaviate_client()
    weaviate_vector_store = weaviate_utils.as_vector_store(weaviate_client, WEAVIATE_CLASS_NAME)
    weaviate_index = VectorStoreIndex.from_vector_store(
        weaviate_vector_store,
    )
    weaviate_retriever = weaviate_index.as_retriever(
        similarity_top_k=SIMILARITY_TOP_K,
        vector_store_query_mode="hybrid",
        alpha=HYBRID_SEARCH_ALPHA,
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
    hyde_llm = OpenAI(model=HYDE_LLM_MODEL, temperature=HYDE_LLM_TEMPERATURE)

    # reranker
    reranker = SentenceTransformerRerank(
        top_n=RERANKED_TOP_N,
        model=RERANKER_MODEL,
    )

    # query pipeline
    qp = QueryPipeline()
    qp.add_modules({
        "original_input": InputComponent(),
        "hyde_prompt_template": hyde_prompt_template,
        "hyde_llm": hyde_llm,
        "hyde_combined_prompt_template": hyde_combined_prompt_template,
        "weaviate_retriever": weaviate_retriever,
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

    return QueryPipelineKnowledgeBaseRetriever.from_defaults(
        query_pipeline=qp,
    )
