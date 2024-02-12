from llama_index import Document, VectorStoreIndex, StorageContext, ServiceContext


def populate_index(docs: list[Document], storage_context: StorageContext | None = None,
                   service_context: ServiceContext | None = None) -> VectorStoreIndex:
    index = VectorStoreIndex(
        nodes=docs,
        storage_context=storage_context,
        service_context=service_context,
        show_progress=True,
    )
    return index
