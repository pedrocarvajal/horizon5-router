from datetime import UTC, datetime
from random import randint
from typing import Any

from django.core.management.base import BaseCommand

from apps.core.repositories.backtest import BacktestRepository


class Command(BaseCommand):
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    help = "Seed a backtest record in MongoDB for testing"

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def handle(self, *_args: Any, **_options: Any) -> None:
        repository = BacktestRepository()

        now = datetime.now(tz=UTC)
        session_id = randint(1000000000, 1999999999)
        backtest_data = {
            "session_id": session_id,
            "asset": "BTCUSDT",
            "created_at": now,
            "end_at": now.replace(second=now.second + 6),
            "start_at": now,
            "status": "completed",
            "updated_at": now.replace(second=now.second + 6),
        }

        try:
            repository.create(backtest_data)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e!r}"))  # type: ignore[attr-defined]
