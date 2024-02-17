from trulens_eval.app import App
from trulens_eval import TruLlama, Feedback
from trulens_eval.feedback import Groundedness, OpenAI

from llama_index.query_engine import BaseQueryEngine

import numpy as np
from typing import Generator, Iterator
import logging

logger = logging.getLogger("EVAL")


def get_eval_dataset_gen(dataset_path: str) -> Generator[str, None, None]:
    with open(dataset_path, "r") as file:
        for line in file:
            yield line


def get_triad_of_metrics_eval_app(app_id: str, query_engine: BaseQueryEngine) -> App:
    # feedback provider
    llm = OpenAI(model_engine="gpt-4")

    # RAG triad of metrics
    context = App.select_context(query_engine)

    # Groundedness: Is the response backed up by the provided context?
    grounded = Groundedness(groundedness_provider=llm)
    f_groundedness = Feedback(
        grounded.groundedness_measure_with_cot_reasons,
        name="Groundedness",
    ).on(context.collect()).on_output().aggregate(grounded.grounded_statements_aggregator)

    # Answer Relevance: How relevant to the input query is the synthesized response?
    f_answer_relevance = Feedback(
        llm.relevance,
        name="Answer Relevance",
    ).on_input().on_output()

    # Context Relevance: How relevant to the input query is the retrieved context?
    f_context_relevance = Feedback(
        llm.qs_relevance,  # relevance of a statement to a question
        name="Context Relevance",
    ).on_input().on(context).aggregate(np.mean)

    return TruLlama(
        app=query_engine,
        app_id=app_id,
        feedbacks=[f_groundedness, f_answer_relevance, f_context_relevance],
    )


def run_eval(query_engine: BaseQueryEngine, eval_app: TruLlama, eval_questions: Iterator[str]) -> None:
    with eval_app as recorder:
        for idx, question in enumerate(eval_questions):
            query_engine.query(question)
            logger.info(f"finished question #{idx + 1}")
