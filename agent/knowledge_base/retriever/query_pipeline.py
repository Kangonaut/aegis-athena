from llama_index.core.query_pipeline import QueryPipeline

from agent.knowledge_base.retriever.base import BaseKnowledgeBaseRetriever, BaseKnowledgeBaseExtractFormatter


class QueryPipelineKnowledgeBaseRetriever(BaseKnowledgeBaseRetriever):
    def __init__(
            self,
            query_pipeline: QueryPipeline,
            formatter: BaseKnowledgeBaseExtractFormatter,
    ) -> None:
        super().__init__(formatter)
        self.query_pipeline = query_pipeline

    def retrieve_raw(self, query: str) -> str:
        return self.query_pipeline.run(input=query)
