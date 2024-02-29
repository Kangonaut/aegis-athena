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
        return UsageAggregation(
            model=entries[0].model,
            service=entries[0].service,
            total_num_tokens=sum(
                map(lambda e: e.num_tokens, entries)
            ),
        ) if entries else None
