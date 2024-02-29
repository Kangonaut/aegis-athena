from abc import ABC, abstractmethod

from usage.base.types import UsageEntry, UsageAggregation


class BaseUsageStore(ABC):
    @abstractmethod
    def add_entry(self, entry: UsageEntry) -> None:
        pass

    @property
    @abstractmethod
    def models(self) -> set[str]:
        pass

    @abstractmethod
    def get_model_entries(self, model_id: str) -> list[UsageEntry] | None:
        pass

    def aggregate_usage(self) -> dict[str, UsageAggregation]:
        return {model_id: self.aggregate_model_usage(model_id) for model_id in self.models}

    def aggregate_model_usage(self, model_id: str) -> UsageAggregation | None:
        entries = self.get_model_entries(model_id)

        # sum up token values
        input_token_sum: int = 0
        output_token_sum: int = 0
        for entry in entries:
            input_token_sum += entry.num_input_tokens
            output_token_sum += entry.num_output_tokens

        return UsageAggregation(
            model=entries[0].model,
            service=entries[0].service,
            num_input_tokens=input_token_sum,
            num_output_tokens=output_token_sum,
        ) if entries else None
