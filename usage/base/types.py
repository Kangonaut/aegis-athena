from abc import abstractmethod
from datetime import datetime

from pydantic import BaseModel, Field


class UsageEntry(BaseModel):
    model: str = Field()
    num_input_tokens: int = Field()
    num_output_tokens: int = Field()
    service: str = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @property
    def model_id(self) -> str:
        return f"{self.service}-{self.model}"


class UsageAggregation(BaseModel):
    model: str = Field()
    num_input_tokens: int = Field()
    num_output_tokens: int = Field()
    service: str = Field()

    @property
    def model_id(self) -> str:
        return f"{self.service}-{self.model}"
