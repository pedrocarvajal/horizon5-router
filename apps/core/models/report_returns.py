from apps.core.models.base import BaseModel
from apps.core.repositories.report_returns import ReportReturnsRepository


class ReportReturnsModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = ReportReturnsRepository()

