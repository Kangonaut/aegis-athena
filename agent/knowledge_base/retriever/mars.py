from llama_index.core import PromptTemplate
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.llms import LLM
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.query_pipeline import QueryPipeline, InputComponent
from llama_index.legacy.postprocessor import BaseNodePostprocessor

from agent.knowledge_base.extract_formatter.base import BaseKnowledgeBaseExtractFormatter
from agent.knowledge_base.extract_formatter.simple import SimpleKnowledgeBaseExtractFormatter
from agent.knowledge_base.retriever.query_pipeline import QueryPipelineKnowledgeBaseRetriever

# Sentence-Window Retrieval
DEFAULT_SENTENCE_WINDOW_RETRIEVAL_TARGET_METADATA_KEY = "window"

# HyDE
DEFAULT_HYDE_PROMPT_TEMPLATE = PromptTemplate(
    "Please write a passage to answer the question\n"
    "Try to include as many key details as possible.\n"
    "\n"
    "{query_str}\n"
    "\n"
    "Passage: "
)
DEFAULT_HYDE_COMBINED_PROMPT_TEMPLATE = PromptTemplate(
    "Question: {query_str}\n"
    "Answer: {hyde_str}"
)


class MarsKnowledgeBaseRetriever(QueryPipelineKnowledgeBaseRetriever):
    def __init__(
            self,
            formatter: BaseKnowledgeBaseExtractFormatter,
            hyde_prompt_template: PromptTemplate,
            hyde_combined_prompt_template: PromptTemplate,
            hyde_llm: LLM,
            retriever: BaseRetriever,
            reranker: BaseNodePostprocessor,
    ) -> None:
        qp = QueryPipeline()
        qp.add_modules({
            "original_input": InputComponent(),
            "hyde_prompt_template": hyde_prompt_template,
            "hyde_llm": hyde_llm,
            "hyde_combined_prompt_template": hyde_combined_prompt_template,
            "retriever": retriever,
            "reranker": reranker,
        })

        # hyde
        qp.add_link("original_input", "hyde_prompt_template", dest_key="query_str")
        qp.add_link("hyde_prompt_template", "hyde_llm")
        qp.add_link("hyde_llm", "hyde_combined_prompt_template", dest_key="hyde_str")
        qp.add_link("original_input", "hyde_combined_prompt_template", dest_key="query_str")
        qp.add_link("hyde_combined_prompt_template", "retriever")

        # reranker
        qp.add_link("retriever", "reranker", dest_key="nodes")
        qp.add_link("original_input", "reranker", dest_key="query_str")

        super().__init__(
            formatter=formatter,
            query_pipeline=qp,
        )

    @classmethod
    def from_defaults(
            cls,
            hyde_llm: LLM,
            retriever: BaseRetriever,
            reranker: BaseNodePostprocessor,

            formatter: BaseKnowledgeBaseExtractFormatter | None = None,

            hyde_prompt_template: PromptTemplate | None = None,
            hyde_combined_prompt_template: PromptTemplate | None = None,
    ) -> "MarsKnowledgeBaseRetriever":
        return cls(
            hyde_llm=hyde_llm,
            retriever=retriever,
            reranker=reranker,

            formatter=formatter or SimpleKnowledgeBaseExtractFormatter(),

            hyde_prompt_template=hyde_prompt_template or DEFAULT_HYDE_PROMPT_TEMPLATE,
            hyde_combined_prompt_template=hyde_combined_prompt_template or DEFAULT_HYDE_COMBINED_PROMPT_TEMPLATE,
        )
