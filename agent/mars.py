from llama_index.core.postprocessor import SentenceTransformerRerank, MetadataReplacementPostProcessor
from llama_index.core import VectorStoreIndex
from llama_index.core.query_pipeline import QueryPipeline, InputComponent
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate
from llama_index.core.response_synthesizers import Refine

from rag import weaviate_utils


def get_v1_0() -> QueryPipeline:
    weaviate_class_name: str = "SentenceWindowDocsChunk"
    similarity_top_k: int = 10
    reranked_top_n: int = 5

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

    reranker = SentenceTransformerRerank(
        top_n=reranked_top_n,
        model="BAAI/bge-reranker-base",
    )

    sentence_window_postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window")

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

    qp.add_link("original_input", "hyde_prompt_template", dest_key="query_str")
    qp.add_link("hyde_prompt_template", "hyde_llm")
    qp.add_link("hyde_llm", "hyde_combined_prompt_template", dest_key="hyde_str")
    qp.add_link("original_input", "hyde_combined_prompt_template", dest_key="query_str")
    qp.add_link("hyde_combined_prompt_template", "weaviate_retriever")

    qp.add_link("weaviate_retriever", "sentence_window_postprocessor", dest_key="nodes")

    qp.add_link("sentence_window_postprocessor", "reranker", dest_key="nodes")
    qp.add_link("original_input", "reranker", dest_key="query_str")

    qp.add_link("reranker", "refine_response_synthesizer", dest_key="nodes")
    qp.add_link("original_input", "refine_response_synthesizer", dest_key="query_str")
    qp.add_link("original_input", "weaviate_retriever")

    return qp
