from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel, Field


class ShellTraceNode(BaseModel):
    timestamp: datetime = Field()
    content: str = Field()


class BaseShellTrace(ABC):
    def __init__(self, trace_id: str):
        self.trace_id = trace_id

    def append(self, node: ShellTraceNode) -> None:
        """add a new node to the trace"""

    @property
    @abstractmethod
    def nodes(self) -> list[ShellTraceNode]:
        """get all nodes in the trace"""
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        pass


class BaseShellTelemetryManager(ABC):
    """manages the creation and retrieval of shell traces"""

    @abstractmethod
    def create(self, trace_id: str) -> BaseShellTrace:
        """create a new shell trace"""
        pass

    @abstractmethod
    def get(self, trace_id: str) -> BaseShellTrace:
        """retrieve an existing shell trace"""
        pass

    @abstractmethod
    def get_all_traces(self) -> list[BaseShellTrace]:
        """get all traces"""
        pass

    @abstractmethod
    def get_all_trace_ids(self) -> list[str]:
        """get all trace IDs"""
        pass
