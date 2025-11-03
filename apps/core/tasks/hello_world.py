from typing import Any

from celery import shared_task

from apps.core.services.logging import LoggingService


@shared_task(name="apps.core.tasks.hello_world")
def hello_world() -> dict[str, Any]:
    logger = LoggingService()
    logger.setup("celery-hello-world")
    logger.info("¡Hola Mundo desde Celery!")
    return {"status": "success", "message": "Hola Mundo"}
