from typing import Sequence, Any, List

from llama_index.core.node_parser import NodeParser
from llama_index.core.schema import BaseNode


class MockNodeParser(NodeParser):
    """
    Does NOT modify provided nodes in any way.

    \\

    Can be used in combination with :code:`HierarchicalNodeParser` to add a relationship between
    the top-level document objects:

    >>> node_parser = HierarchicalNodeParser.from_defaults(
    >>>     node_parser_ids=["mock", "other"],
    >>>     node_parser_map={
    >>>         "mock": MockNodeParser(),
    >>>         "other": <NODE-PARSER>
    >>>     }
    >>> )
    """

    def _parse_nodes(self, all_nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any) -> List[BaseNode]:
        return list(all_nodes)
