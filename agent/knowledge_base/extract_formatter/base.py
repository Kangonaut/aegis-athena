from abc import ABC, abstractmethod

from llama_index.core.schema import NodeWithScore


class BaseKnowledgeBaseExtractFormatter(ABC):
    @abstractmethod
    def format(self, nodes: list[NodeWithScore]) -> str:
        pass
