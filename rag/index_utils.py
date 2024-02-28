from llama_index.core import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.core.base.embeddings.base import BaseEmbedding


def populate_index(docs: list[Document], storage_context: StorageContext | None = None,
                   embed_model: BaseEmbedding | None = None) -> VectorStoreIndex:
    index = VectorStoreIndex(
        nodes=docs,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
    )
    return index
