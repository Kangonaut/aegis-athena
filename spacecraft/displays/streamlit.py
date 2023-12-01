import io

from spacecraft.displays.base import BaseDisplay


class StreamlitDisplay(BaseDisplay):
    __KEYWORD_COLORS: dict[str, str] = {
        "ERROR": "red",
        "OFFLINE": "red",
        "MALFUNC": "orange",
        "MALFUNCTION": "orange",
        "NOMINAL": "green",
    }

    def __init__(self):
        self.__out_stream = io.StringIO()
        self.__last_read_pos: int = 0

    def __highlight_keywords(self, content: str) -> str:
        for keyword, color in self.__KEYWORD_COLORS.items():
            content = content.replace(keyword, f":{color}[{keyword}]")
        return content

    def __transform_input(self, content: str) -> str:
        # replace space
        content = content.replace(" ", "&nbsp;")

        # replace newline
        content = content.replace("\n", "\n\n")

        # color code keywords
        content = self.__highlight_keywords(content)

        return content

    def print(self, content: str) -> None:
        print(content, file=self.__out_stream, end="\n")

    def read_recent(self) -> str:
        # go back to last read position
        self.__out_stream.seek(self.__last_read_pos)

        # read
        content = self.__out_stream.read()
        content = self.__transform_input(content)

        # update last read position
        self.__last_read_pos = self.__out_stream.tell()

        return content
