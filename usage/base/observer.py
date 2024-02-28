from abc import ABC

from usage.base.usage_store import BaseUsageStore


class BaseUsageObserver(ABC):
    def __init__(self, store: BaseUsageStore) -> None:
        self._store = store
