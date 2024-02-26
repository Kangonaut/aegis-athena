import io
import time
from typing import Callable

from spacecraft.displays.base import BaseDisplay


class StreamlitDisplay(BaseDisplay):
    __KEYWORD_COLORS: dict[str, str] = {
        "OFFLINE": "red",
        "MALFUNC": "orange",
        "MALFUNCTION": "orange",
        "NOMINAL": "green",
        "DEBUG": "gray",
        "INFO": "blue",
        "WARNING": "orange",
        "ERROR": "red",
    }

    def __init__(self, callback: Callable[[str], None]):
        self.__out_stream = io.StringIO()
        self.__callback = callback

    def __highlight_keywords(self, content: str) -> str:
        for keyword, color in self.__KEYWORD_COLORS.items():
            content = content.replace(keyword, f":{color}[{keyword}]")
        return content

    def __transform_input(self, content: str) -> str:
        # replace command prefix
        content = content.replace("system:/ $", "**:violet[system]:/ $**")

        # replace space
        content = content.replace(" ", "   ")

        # replace newline
        content = content.replace("\n", "\n\n")

        # color code keywords
        content = self.__highlight_keywords(content)

        return content

    def print(self, content: str, end="\n") -> None:
        # transform input
        content = self.__transform_input(f"{content}{end}")

        # print to out-stream
        print(content, file=self.__out_stream, end="")

        # call callback and pass output up to this point
        content = self.__out_stream.getvalue()
        self.__callback(content)

    def flush(self) -> str:
        content = self.__out_stream.getvalue()
        self.__out_stream = io.StringIO()
        return content
