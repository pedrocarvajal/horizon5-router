from datetime import UTC, datetime
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
        limit: int = 10,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_direction: str = "desc",
        query_filters: Optional[Dict[str, Any]] = None,
        projection_fields: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        collection = self._db_service.get_collection(self._collection_name)
        filters = query_filters or {}
        projection = projection_fields or {}
        cursor = collection.find(filters, projection)

        if sort_by and sort_direction:
            direction = -1 if sort_direction == "desc" else 1
            cursor = cursor.sort(sort_by, direction)

        if offset:
            cursor = cursor.skip(offset)

        if limit != 9**100:
            cursor = cursor.limit(limit)

        return list(cursor)

    def count(
        self,
        query_filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        collection = self._db_service.get_collection(self._collection_name)
        filters = query_filters or {}
        return collection.count_documents(filters)

    def store(
        self,
        data: Dict[str, Any],
    ) -> str:
        if "created_at" in data and not isinstance(data["created_at"], datetime):
            created_at = data["created_at"]
            created_at = float(created_at if created_at is not None else 0)
            data["created_at"] = datetime.fromtimestamp(created_at, tz=UTC)
        elif "created_at" not in data:
            data["created_at"] = datetime.now(tz=UTC)

        if "updated_at" in data and not isinstance(data["updated_at"], datetime):
            updated_at = data["updated_at"]
            updated_at = float(updated_at if updated_at is not None else 0)
            data["updated_at"] = datetime.fromtimestamp(updated_at, tz=UTC)
        elif "updated_at" not in data:
            data["updated_at"] = datetime.now(tz=UTC)

        collection = self._db_service.get_collection(self._collection_name)
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def store_many(
        self,
        data: List[Dict[str, Any]],
    ) -> List[str]:
        now = datetime.now(tz=UTC)

        for item in data:
            if "created_at" in item and not isinstance(item["created_at"], datetime):
                created_at = item["created_at"]
                created_at = float(created_at if created_at is not None else 0)
                item["created_at"] = datetime.fromtimestamp(created_at, tz=UTC)
            elif "created_at" not in item:
                item["created_at"] = now

            if "updated_at" in item and not isinstance(item["updated_at"], datetime):
                updated_at = item["updated_at"]
                updated_at = float(updated_at if updated_at is not None else 0)
                item["updated_at"] = datetime.fromtimestamp(updated_at, tz=UTC)
            elif "updated_at" not in item:
                item["updated_at"] = now

        collection = self._db_service.get_collection(self._collection_name)
        result = collection.insert_many(data)
        return [str(inserted_id) for inserted_id in result.inserted_ids]

    def update(
        self,
        query_filters: Dict[str, Any],
        data: Dict[str, Any],
    ) -> int:
        if "updated_at" in data and not isinstance(data["updated_at"], datetime):
            updated_at = data["updated_at"]
            updated_at = float(updated_at if updated_at is not None else 0)
            data["updated_at"] = datetime.fromtimestamp(updated_at, tz=UTC)
        elif "updated_at" not in data:
            data["updated_at"] = datetime.now(tz=UTC)

        collection = self._db_service.get_collection(self._collection_name)
        result = collection.update_one(query_filters, {"$set": data})
        return result.modified_count

    def delete(
        self,
        query_filters: Dict[str, Any],
    ) -> int:
        collection = self._db_service.get_collection(self._collection_name)
        result = collection.delete_one(query_filters)
        return result.deleted_count

    def delete_many(
        self,
        query_filters: Dict[str, Any],
    ) -> int:
        collection = self._db_service.get_collection(self._collection_name)
        result = collection.delete_many(query_filters)
        return result.deleted_count
