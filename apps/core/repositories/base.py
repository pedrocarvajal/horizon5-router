from typing import Any, Dict, List, Optional

from apps.core.interfaces.repository import RepositoryInterface
from apps.core.services.mongodb import MongoDBService


class BaseRepository(RepositoryInterface):
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _collection_name: str
    _db_service: MongoDBService

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self, collection_name: str) -> None:
        self._collection_name = collection_name
        self._db_service = MongoDBService()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def find(
        self,
        filters: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        collection = self._db_service.get_collection(self._collection_name)
        query_filters = filters or {}
        query_projection = projection or {}
        cursor = collection.find(query_filters, query_projection)

        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def create(self, data: Dict[str, Any]) -> str:
        collection = self._db_service.get_collection(self._collection_name)
        result = collection.insert_one(data)
        return str(result.inserted_id)
