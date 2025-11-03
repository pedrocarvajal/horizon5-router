from apps.core.models.base import BaseModel
from apps.core.repositories.report_performance import ReportPerformanceRepository


class ReportPerformanceModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = ReportPerformanceRepository()
