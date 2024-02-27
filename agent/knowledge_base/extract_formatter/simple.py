from llama_index.core.schema import NodeWithScore

from agent.knowledge_base.extract_formatter.base import BaseKnowledgeBaseExtractFormatter


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
