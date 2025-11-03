import logging
from datetime import UTC, datetime
from typing import Any

from celery import shared_task

from apps.core.repositories.backtest import BacktestRepository
from apps.core.repositories.order import OrderRepository
from apps.core.repositories.report import ReportRepository

logger = logging.getLogger("django")


class ProcessBacktestTask:
    _name: str = "process_backtest"

    def __init__(self) -> None:
        self._backtest_repository = BacktestRepository()
        self._report_repository = ReportRepository()
        self._order_repository = OrderRepository()

    def run(self) -> None:
        logger.info(f"Processing task: {self._name}")


@shared_task(name="apps.core.tasks.process_backtest")
def process_backtest() -> dict[str, Any]:
    task = ProcessBacktestTask()
    task.run()

    return {
        "status": "success",
        "time": datetime.now(tz=UTC),
    }
