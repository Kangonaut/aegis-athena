from llama_index import Document, VectorStoreIndex, StorageContext


def populate_index(storage_context: StorageContext, docs: list[Document]) -> VectorStoreIndex:
    index = VectorStoreIndex(
        nodes=docs,
        storage_context=storage_context,
        show_progress=True,
    )
    return index
