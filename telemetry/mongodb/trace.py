from datetime import datetime

from pymongo.collection import Collection

from telemetry.base import BaseShellTrace, ShellTraceNode


class MongoDbShellTrace(BaseShellTrace):

    def __init__(
            self,
            trace_id: str,
            collection: Collection,
    ):
        super().__init__(trace_id)
        self._collection = collection

        # check if document exists
        if not self.__retrieve_document():
            self.__create_document()

        self._cache = None

    def __create_document(self) -> None:
        self._collection.insert_one({
            "_id": self.trace_id,
            "timestamp": datetime.utcnow(),
            "nodes": [],
        })

    def __get_document(self) -> dict[str, any]:
        # check cache
        if not self._cache:
            # check if document exists
            if not (document := self.__retrieve_document()):
                self.__create_document()
                document = self.__retrieve_document()
            self._cache = document
        return self._cache

    def __invalidate_cache(self) -> None:
        self._cache = None

    def __retrieve_document(self) -> dict[str, any] | None:
        document = self._collection.find_one(
            filter={
                "_id": self.trace_id,
            }
        )
        return document

    def append(self, node: ShellTraceNode) -> None:
        self._collection.find_one_and_update(
            filter={
                "_id": self.trace_id,
            },
            update={
                "$push": {
                    "nodes": node.model_dump(),  # node as dict
                }
            }
        )
        self.__invalidate_cache()

    @property
    def nodes(self) -> list[ShellTraceNode]:
        document = self.__get_document()
        return [ShellTraceNode.model_validate(node) for node in document["nodes"]]  # parse using pydantic

    @property
    def timestamp(self) -> datetime:
        document = self.__get_document()
        return document["timestamp"]
