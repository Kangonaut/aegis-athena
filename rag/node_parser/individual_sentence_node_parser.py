from typing import Callable, List, Optional, Sequence, Any

from llama_index.core import Document
from llama_index.core.callbacks import CallbackManager
from llama_index.core.node_parser import NodeParser, SentenceWindowNodeParser
from llama_index.core.node_parser.node_utils import default_id_func, build_nodes_from_splits
from llama_index.core.node_parser.text.utils import split_by_sentence_tokenizer
from llama_index.core.schema import BaseNode
from llama_index.core.utils import get_tqdm_iterable
from pydantic import Field


class IndividualSentenceNodeParser(NodeParser):
    """
    Splits a document into nodes, with each node being a sentence.
    """

    sentence_splitter: Callable[[str], List[str]] = Field(
        default_factory=split_by_sentence_tokenizer,
        description="The text splitter to use when splitting documents.",
        exclude=True,
    )

    @classmethod
    def class_name(cls) -> str:
        return "IndividualSentenceNodeParser"

    @classmethod
    def from_defaults(
            cls,
            sentence_splitter: Optional[Callable[[str], List[str]]] = None,
            include_metadata: bool = True,
            include_prev_next_rel: bool = True,
            callback_manager: Optional[CallbackManager] = None,
            id_func: Optional[Callable[[int, Document], str]] = None,
    ) -> "IndividualSentenceNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()

        id_func = id_func or default_id_func

        return cls(
            sentence_splitter=sentence_splitter,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
            id_func=id_func,
        )

    def _parse_nodes(
            self,
            nodes: Sequence[BaseNode],
            show_progress: bool = False,
            **kwargs: Any,
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            nodes = self.build_sentence_nodes_from_documents([node])
            all_nodes.extend(nodes)

        return all_nodes

    def build_sentence_nodes_from_documents(
            self, documents: Sequence[Document]
    ) -> List[BaseNode]:
        """Build window nodes from documents."""
        all_nodes: List[BaseNode] = []

        for document in documents:
            # sentence splitting
            text_splits = self.sentence_splitter(document.text)

            # remove leading and trailing whitespace
            text_splits = [split.strip() for split in text_splits]

            # build nodes
            nodes = build_nodes_from_splits(
                text_splits,
                document,
                id_func=self.id_func,
            )
            all_nodes.extend(nodes)

        return all_nodes
