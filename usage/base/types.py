from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class BaseUsageEntry(ABC, BaseModel):
    model: str = Field()
    num_tokens: int = Field()

    @property
    @abstractmethod
    def service_id(self) -> str:
        pass

    @property
    def model_id(self) -> str:
        return f"{self.service_id}-{self.model}"


class UsageAggregation(BaseModel):
    model: str = Field()
    total_num_tokens: int = Field()
    service_id: str = Field()

    @property
    def model_id(self) -> str:
        return f"{self.service_id}-{self.model}"
