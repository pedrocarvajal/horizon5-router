from apps.core.models.base import BaseModel
from apps.core.repositories.backtest import BacktestRepository


class BacktestModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = BacktestRepository()
