from urllib.parse import urlparse

from arq import cron
from arq.connections import RedisSettings

from secret_rotator.config import settings
from secret_rotator.worker.tasks import (
    check_rotation_schedules,
    execute_rotation_pipeline,
    retire_old_credential,
)


def get_redis_settings() -> RedisSettings:
    parsed = urlparse(settings.REDIS_URL)
    return RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
        database=int(parsed.path.lstrip("/") or "0"),
        password=parsed.password,
    )


async def startup(ctx: dict) -> None:
    from secret_rotator.database import async_session_factory
    from secret_rotator.encryption import encryption
    from secret_rotator.redis_client import redis_client
    from secret_rotator.services.rollback_service import RollbackService
    from secret_rotator.services.rotation_orchestrator import RotationOrchestrator
    from secret_rotator.services.schedule_service import ScheduleService

    ctx["orchestrator"] = RotationOrchestrator(
        session_factory=async_session_factory,
        redis=redis_client,
        encryption=encryption,
        settings=settings,
    )
    ctx["rollback_service"] = RollbackService(
        session_factory=async_session_factory,
        encryption=encryption,
    )
    ctx["schedule_service"] = ScheduleService(
        session_factory=async_session_factory,
    )


async def shutdown(ctx: dict) -> None:
    pass


class WorkerSettings:
    functions = [execute_rotation_pipeline, retire_old_credential]
    cron_jobs = [
        cron(
            check_rotation_schedules,
            minute={0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55},
        )
    ]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = get_redis_settings()
    max_jobs = settings.ARQ_MAX_JOBS
