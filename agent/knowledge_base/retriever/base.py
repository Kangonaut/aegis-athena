from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from llama_index.core import QueryBundle
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.callbacks import CallbackManager
from llama_index.core.schema import NodeWithScore, IndexNode

from agent.knowledge_base.extract_formatter.base import BaseKnowledgeBaseExtractFormatter


class BaseKnowledgeBaseRetriever(BaseRetriever, ABC):
    def __init__(
            self,
            formatter: BaseKnowledgeBaseExtractFormatter,

            callback_manager: Optional[CallbackManager] = None,
            object_map: Optional[Dict] = None,
            objects: Optional[List[IndexNode]] = None,
            verbose: bool = False,
    ) -> None:
        super().__init__(
            callback_manager=callback_manager,
            object_map=object_map,
            objects=objects,
            verbose=verbose,
        )
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

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        return self.retrieve_raw(query_bundle.query_str)
