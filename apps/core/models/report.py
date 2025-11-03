from apps.core.models.base import BaseModel
from apps.core.repositories.report import ReportRepository


class ReportModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = ReportRepository()
