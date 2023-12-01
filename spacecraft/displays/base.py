import abc


class BaseDisplay(abc.ABC):
    @abc.abstractmethod
    def print(self, content: str) -> None:
        pass
