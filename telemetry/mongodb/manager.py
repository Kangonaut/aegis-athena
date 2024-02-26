from telemetry.base import BaseShellTelemetryManager
from telemetry.mongodb import utils
from telemetry.mongodb.trace import MongoDbShellTrace

from pymongo.database import Database

from pymongo.collection import Collection

DEFAULT_COLLECTION_NAME: str = "shell-traces"


class MongoDbShellTelemetryManager(BaseShellTelemetryManager):
    """manages the creation and retrieval of shell traces"""

    def __init__(
            self,
            database: Database | None = None,
            collection_name: str | None = None,
    ):
        self._database = database

        # create collection if it does not exist
        self._collection: Collection = self._database[collection_name]

    @classmethod
    def from_defaults(
            cls,
            database: Database | None = None,
            collection_name: str | None = None,
    ) -> "MongoDbShellTelemetryManager":
        return cls(
            database=database or utils.get_database(),
            collection_name=collection_name or DEFAULT_COLLECTION_NAME,
        )

    def create(self, trace_id: str) -> MongoDbShellTrace:
        """create a new shell trace"""
        return MongoDbShellTrace(
            collection=self._collection,
            trace_id=trace_id,
        )

    def get(self, trace_id: str) -> MongoDbShellTrace:
        """retrieve an existing shell trace"""
        return MongoDbShellTrace(
            collection=self._collection,
            trace_id=trace_id,
        )

    def get_all_traces(self) -> list[MongoDbShellTrace]:
        trace_ids: list[str] = self.get_all_trace_ids()
        return [
            MongoDbShellTrace(
                collection=self._collection,
                trace_id=trace_id,
            )
            for trace_id in trace_ids
        ]

    def get_all_trace_ids(self) -> list[str]:
        cursor = self._collection.find(
            projection={"_id": 1}
        )
        return [document["_id"] for document in cursor]
