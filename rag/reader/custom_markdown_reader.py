import re
from pathlib import Path
from typing import List, Optional, Tuple, cast, Dict, Any

from fsspec import AbstractFileSystem
from llama_index.core import Document
from llama_index.readers.file import MarkdownReader
from pydantic import Field

DEFAULT_SECTION_TITLE_METADATA_KEY: str = "section_title"


class CustomMarkdownReader(MarkdownReader):
    """
    Based on the default :code:`MarkdownReader`, but with the following adjustments:

    \\

    Text in diamond operators (:code:`\"<.*>\"`) is NOT being removed.
    This behavior is used in the original :code:`MarkdownReader` to remove HTML tags.
    However, it also removes placeholders syntax (e.g.: :code:`ping <IP-ADDRESS>`) from command documentation.
    This behavior is removed from this custom version.

    \\


    """
    section_title_metadata_key: str = Field(
        default=DEFAULT_SECTION_TITLE_METADATA_KEY,
        description="The metadata key to store the section title under."
    )

    @classmethod
    def from_defaults(
            cls,
            section_title_metadata_key: str = DEFAULT_SECTION_TITLE_METADATA_KEY,
            add_section_title_metadata: bool = True,
    ) -> "CustomMarkdownReader":

        return cls(
            section_title_metadata_key=section_title_metadata_key,
            add_section_title_metadata=add_section_title_metadata,
        )

    def __init__(
            self,
            *args: Any,
            add_section_title_metadata: bool,
            section_title_metadata_key: str,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._add_section_title_metadata = add_section_title_metadata
        self.section_title_metadata_key = section_title_metadata_key

    def markdown_to_tups(self, markdown_text: str) -> List[Tuple[Optional[str], str]]:
        """Convert a markdown file to a dictionary.

        The keys are the headers and the values are the text under each header.

        """
        markdown_tups: List[Tuple[Optional[str], str]] = []
        lines = markdown_text.split("\n")

        current_header = None
        current_text = ""

        for line in lines:
            header_match = re.match(r"^#+\s", line)
            if header_match:
                if current_header is not None:
                    if current_text == "" or None:
                        continue
                    markdown_tups.append((current_header, current_text))

                current_header = line
                current_text = ""
            else:
                current_text += line + "\n"
        markdown_tups.append((current_header, current_text))

        if current_header is not None:
            # pass linting, assert keys are defined
            markdown_tups = [
                (re.sub(r"#", "", cast(str, key)).strip(), value)
                for key, value in markdown_tups
            ]
        else:
            markdown_tups = [
                (key, value) for key, value in markdown_tups
            ]

        return markdown_tups

    def load_data(
            self,
            file: Path,
            extra_info: Optional[Dict] = None,
            fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
        """Parse file into string."""
        tups = self.parse_tups(file, fs=fs)
        results = []

        for header, value in tups:
            if header is None:
                results.append(Document(text=value, metadata=extra_info or {}))
            else:
                if self._add_section_title_metadata:
                    # add section title to metadata
                    # NOTE: the section title is NOT excluded from llm and embed
                    metadata = extra_info or {}
                    metadata[self.section_title_metadata_key] = header

                results.append(
                    Document(text=f"{header}\n{value}", metadata=extra_info or {})
                )
        return results
