import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId
from celery import shared_task

from apps.core.enums.backtest_status import BacktestStatus
from apps.core.enums.report_status import ReportStatus
from apps.core.repositories.backtest import BacktestRepository
from apps.core.repositories.order import OrderRepository
from apps.core.repositories.report import ReportRepository
from apps.core.repositories.snapshot import SnapshotRepository

logger = logging.getLogger("django")


class ProcessBacktestTask:
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _name: str = "process_backtest"
    _backtest: Dict[str, Any]
    _report: Optional[Dict[str, Any]]
    _orders: List[Dict[str, Any]]
    _snapshots: List[Dict[str, Any]]

    _allocation: float

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        self._backtest_repository = BacktestRepository()
        self._report_repository = ReportRepository()
        self._order_repository = OrderRepository()
        self._snapshot_repository = SnapshotRepository()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def run(self) -> None:
        pending_backtests = self._get_pending_backtests()

        for backtest in pending_backtests:
            backtest_id = str(backtest["_id"])
            session_id = backtest["session_id"]
            report_id = None
            report = self._get_report_by_backtest_id(backtest_id)

            if report:
                report_id = report["_id"]

                if report["status"] == ReportStatus.FAILED.value:
                    logger.info(
                        f"Ignoring backtest: {backtest_id}, "
                        f"report status: {report['status']} "
                        f"Because it failed before."
                    )

                    continue

                if report["status"] == ReportStatus.READY.value:
                    logger.info(
                        f"Ignoring backtest: {backtest_id}, "
                        f"report status: {report['status']} "
                        f"Because it is already ready."
                    )

                    continue

                if report["status"] == ReportStatus.BUILDING.value:
                    logger.info(
                        f"Ignoring backtest: {backtest_id}, "
                        f"report status: {report['status']} "
                        f"Because it is already building."
                    )

                    continue

            else:
                report_id = self._create_report(
                    {
                        "backtest_id": backtest_id,
                        "status": ReportStatus.BUILDING.value,
                    }
                )

                logger.info(report_id)

                report = self._get_report_by_id(report_id)

                logger.info(report)

                if not report:
                    logger.error(f"Failed to create report for backtest {backtest_id}")

                    self._update_report(
                        report_id=report_id,
                        data={
                            "status": ReportStatus.FAILED.value,
                        },
                    )

                    continue

            self._backtest = backtest
            self._report = report
            self._orders = self._get_orders_by_backtest_id(session_id)
            self._snapshots = self._get_snapshots_by_backtest_id(session_id)
            self._allocation = self._snapshots[0]["allocation"]

            backtest_id = self._backtest["_id"]
            session_id = self._backtest["session_id"]
            report_id = self._report["_id"]
            orders = self._orders
            snapshots = self._snapshots
            allocation = self._allocation

            logger.info(f"Backtest id: {backtest_id}")
            logger.info(f"Session id: {session_id}")
            logger.info(f"Report id: {report_id}")
            logger.info(f"Orders count: {len(orders)}")
            logger.info(f"Snapshots count: {len(snapshots)}")
            logger.info(f"Allocation: {allocation:,.2f}")

            self._update_report(
                report_id=report_id,
                data={
                    "status": ReportStatus.READY.value,
                },
            )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _get_cumulative_returns_from_orders(
        self,
        orders: List[Dict[str, Any]],
        allocation: float,
    ) -> Tuple[List[float], List[float], List[datetime]]:
        cumulative_returns = []
        capital_growth_percentage = []
        dates = []
        total = 0.0

        for order in orders:
            total += order.get("profit", 0.0)
            cumulative_returns.append(total)
            growth_pct = ((allocation + total) / allocation - 1) * 100
            capital_growth_percentage.append(growth_pct)
            dates.append(order.get("created_at"))

        return cumulative_returns, capital_growth_percentage, dates

    def _get_pending_backtests(self) -> List[Dict[str, Any]]:
        return self._backtest_repository.find(
            query_filters={
                "status": BacktestStatus.COMPLETED.value,
            },
        )

    def _get_report_by_backtest_id(self, backtest_id: str) -> Optional[Dict[str, Any]]:
        report = self._report_repository.find(
            query_filters={"backtest_id": backtest_id},
        )

        return report[0] if report else None

    def _get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        report = self._report_repository.find(
            query_filters={"_id": ObjectId(report_id)},
        )

        return report[0] if report else None

    def _get_orders_by_backtest_id(self, session_id: str) -> List[Dict[str, Any]]:
        return self._order_repository.find(
            limit=9**100,
            query_filters={
                "backtest": True,
                "backtest_id": session_id,
            },
        )

    def _get_snapshots_by_backtest_id(self, session_id: str) -> List[Dict[str, Any]]:
        return self._snapshot_repository.find(
            limit=9**100,
            query_filters={"session_id": session_id},
        )

    def _create_report(self, data: Dict[str, Any]) -> str:
        return self._report_repository.store(
            data=data,
        )

    def _update_report(self, report_id: str, data: Dict[str, Any]) -> None:
        self._report_repository.update(
            query_filters={"_id": ObjectId(report_id)},
            data=data,
        )


@shared_task(name="apps.core.tasks.process_backtest")
def process_backtest() -> Dict[str, Any]:
    task = ProcessBacktestTask()
    task.run()

    return {
        "status": "success",
        "time": datetime.now(tz=UTC),
    }
