from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class RepositoryInterface(ABC):
    @abstractmethod
    def find(
        self,
        filters: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> str:
        pass
