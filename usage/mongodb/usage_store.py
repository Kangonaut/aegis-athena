from usage.base.types import UsageEntry
from usage.base.usage_store import BaseUsageStore

from pymongo import MongoClient

DEFAULT_DB_NAME: str = "db_usage_store"
DEFAULT_COLLECTION_NAME: str = "data"


class MongoDBUsageStore(BaseUsageStore):

    def __init__(
            self,
            mongodb_client: MongoClient,
            db_name: str | None = None,
    ) -> None:
        self._client = mongodb_client
        self._db_name = db_name or DEFAULT_DB_NAME
        self._db = self._client[self._db_name]
        self._collection = self._db[DEFAULT_COLLECTION_NAME]

    @classmethod
    def from_uri(
            cls,
            uri: str,
            db_name: str | None = None,
    ) -> "MongoDBUsageStore":
        mongodb_client = MongoClient(uri)
        return cls(
            mongodb_client=mongodb_client,
            db_name=db_name,
        )

    @classmethod
    def from_host_and_port(
            cls,
            host: str,
            port: int,
            db_name: str | None = None,
    ) -> "MongoDBUsageStore":
        mongodb_client = MongoClient(host=host, port=port)
        return cls(
            mongodb_client=mongodb_client,
            db_name=db_name,
        )

    def add_entry(
            self,
            entry: UsageEntry
    ) -> None:
        data = {
            "model_id": entry.model_id,
            **entry.model_dump(),
        }
        self._collection.insert_one(data)

    @property
    def models(self) -> set[str]:
        result = self._collection.aggregate([
            {
                "$group": {
                    "_id": "$model_id",
                },
            },
        ])
        return {doc.get("_id") for doc in result}

    def get_model_entries(self, model_id: str) -> list[UsageEntry] | None:
        result = self._collection.find({
            "model_id": model_id,
        })
        entries: list[UsageEntry] = []
        for doc in result:
            doc.pop("model_id")
            entry = UsageEntry(**doc)
            entries.append(entry)
        return entries
