from llama_index.core import SimpleDirectoryReader, Document

import os

from rag.reader.custom_markdown_reader import CustomMarkdownReader


def load_data_dir(dir_path: str) -> list[Document]:
    dir_path: str = os.path.join(dir_path)
    reader = SimpleDirectoryReader(
        input_dir=dir_path,
        file_extractor={
            ".md": CustomMarkdownReader.from_defaults(),
        },
        required_exts=[".md"],
    )
    return reader.load_data()


def group_documents(documents: list[Document], group_by: str) -> dict[str, list[Document]]:
    """
    Groups documents together based on a metadata attribute, identified by the :code:`group_by` parameter.
    """
    grouped_documents: dict[str, list[Document]] = {}
    for document in documents:
        key: str = document.metadata[group_by]
        if key not in grouped_documents:
            grouped_documents[key] = []
        grouped_documents[key].append(document)
    return grouped_documents


def join_grouped_documents(grouped_documents: dict[str, list[Document]]) -> dict[str, Document]:
    """
    Joins grouped documents into a single document object.
    """
    return {key: Document(
        text="".join(map(lambda x: x.text, documents))
    ) for key, documents in grouped_documents.items()}
