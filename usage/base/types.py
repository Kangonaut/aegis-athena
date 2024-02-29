from abc import abstractmethod

from pydantic import BaseModel, Field


class UsageEntry(BaseModel):
    model: str = Field()
    num_tokens: int = Field()
    service: str = Field()

    @property
    def model_id(self) -> str:
        return f"{self.service}-{self.model}"


class UsageAggregation(BaseModel):
    model: str = Field()
    total_num_tokens: int = Field()
    service: str = Field()

    @property
    def model_id(self) -> str:
        return f"{self.service}-{self.model}"
