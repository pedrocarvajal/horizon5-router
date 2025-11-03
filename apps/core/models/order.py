from apps.core.models.base import BaseModel
from apps.core.repositories.order import OrderRepository


class OrderModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self._repository = OrderRepository()
