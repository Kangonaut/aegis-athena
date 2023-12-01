import abc


class BaseDisplay(abc.ABC):
    @abc.abstractmethod
    def print(self, string: str) -> None:
        pass
