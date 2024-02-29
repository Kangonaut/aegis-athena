from usage.base.types import UsageEntry, UsageAggregation
from usage.base.usage_store import BaseUsageStore


class SimpleUsageStore(BaseUsageStore):
    def __init__(self):
        self._entries: dict[str, list[UsageEntry]] = {}

    def add_entry(self, entry: UsageEntry) -> None:
        key = entry.model_id
        if key not in self._entries:
            self._entries[key] = []
        self._entries[key].append(entry)

    @property
    def models(self) -> set[str]:
        return set(self._entries.keys())

    def get_model_entries(self, model_id: str) -> list[UsageEntry] | None:
        return self._entries.get(model_id)

    def aggregate_usage(self) -> dict[str, UsageAggregation]:
        return {model_id: self.aggregate_model_usage(model_id) for model_id in self.models}
