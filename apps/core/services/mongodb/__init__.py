from typing import Any, Optional

from django.conf import settings
from pymongo import MongoClient
from pymongo.database import Database


class MongoDBService:
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _instance: Optional["MongoDBService"] = None
    _connection: Optional[MongoClient] = None
    _database: Optional[Database] = None

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __new__(cls) -> "MongoDBService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._connection is None:
            self._connect()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def get_collection(self, collection_name: str) -> Any:
        if self._database is None:
            self._connect()

        if self._database is None:
            raise ConnectionError("Failed to connect to MongoDB")

        return self._database[collection_name]

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _connect(self) -> None:
        mongodb_config = settings.DATABASES["mongodb"]

        db_name = mongodb_config["DB_NAME"]
        db_user = mongodb_config["DB_USER"]
        db_password = mongodb_config["DB_PASSWORD"]
        db_host = mongodb_config["DB_HOST"]
        db_port = mongodb_config["DB_PORT"]

        uri = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/"

        self._connection = MongoClient(uri)
        self._database = self._connection[db_name]
