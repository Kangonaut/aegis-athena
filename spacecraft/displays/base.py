import abc


class BaseDisplay(abc.ABC):
    @abc.abstractmethod
    def print(self, content: str, end="\n") -> None:
        pass

    @abc.abstractmethod
    def flush(self) -> str:
        pass

    def debug(self, content: str, end="\n") -> None:
        self.print(f"DEBUG: {content}", end=end)

    def info(self, content: str, end="\n") -> None:
        self.print(f"INFO: {content}", end=end)

    def warning(self, content: str, end="\n") -> None:
        self.print(f"WARNING: {content}", end=end)

    def error(self, content: str, end="\n") -> None:
        self.print(f"ERROR: {content}", end=end)
