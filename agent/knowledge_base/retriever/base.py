from abc import ABC, abstractmethod

from llama_index.core.schema import NodeWithScore

from agent.knowledge_base.extract_formatter.base import BaseKnowledgeBaseExtractFormatter


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
