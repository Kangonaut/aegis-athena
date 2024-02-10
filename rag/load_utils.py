from llama_index import SimpleDirectoryReader
from llama_index import Document

import os


def load_data_dir(dir_path: str) -> list[Document]:
    dir_path: str = os.path.join(dir_path)
    reader = SimpleDirectoryReader(
        input_dir=dir_path,
        required_exts=[".md"],
    )
    return reader.load_data()
