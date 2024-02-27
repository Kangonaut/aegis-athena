import re
from typing import List, Optional, Tuple, cast

from llama_index.readers.file import MarkdownReader


class CustomMarkdownReader(MarkdownReader):
    """
    Essentially the same as :code:`MarkdownReader`, but does not remove text in diamond operators (:code:`\"<.*>\"`).

    \\

    This behavior is used in the original :code:`MarkdownReader` to remove HTML tags.
    However, it also removes placeholders syntax (e.g.: :code:`ping <IP-ADDRESS>`) from command documentation.
    This behavior is removed from this custom version.
    """

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
