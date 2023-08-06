from __future__ import annotations

__all__ = ["WorkerSettings", "create_worker"]

import logging
import datetime
from typing import Sequence, Type, Any
from types import ModuleType
from arq.worker import Worker, Function
from arq.typing import WorkerCoroutine, StartupShutdown, SecondsTimedelta
from arq.jobs import Serializer, Deserializer
from arq.cron import CronJob
from arq.connections import RedisSettings, ArqRedis

from .config import QueueSettings
from .context import Context, init_context, close_context
from .utils import get_tasks

logger: logging.Logger = logging.getLogger(name="pool_cue")

WorkerSettings = Type[Worker]


async def on_startup(ctx: Context) -> Context:
    """Initialize a new thread pool executor in the worker context."""
    return await init_context(ctx=ctx)


async def on_shutdown(ctx: Context) -> None:
    """Shut down the thread pool executor in the worker context."""
    await close_context(ctx=ctx)


def create_worker(
    settings: QueueSettings,
    tasks: ModuleType | Sequence[ModuleType],
    **kwargs,
) -> WorkerSettings:
    """
    Create a new arq worker settings class that is used to create/ run workers using the arq cli.

    Example Usage:

    >>> from pool_cue import QueueSettings, create_worker
    >>> settings = QueueSettings(...)
    >>> Worker = create_worker(settings=settings, tasks=...)

    And run 'arq path.to.file.Worker' from the command line to start the worker(s).

    :param settings: Queue settings.
    :param tasks: Module(s) containing task functions to register.
    :param kwargs: Extra worker settings, see `arq.worker.Worker` for details.
    """

    class Settings(Worker):
        functions: Sequence[Function | WorkerCoroutine] = get_tasks(modules=tasks)
        queue_name: str = kwargs.get("queue_name", settings.queue_name)
        cron_jobs: Sequence[CronJob] | None = kwargs.get("cron_jobs", None)
        redis_settings: RedisSettings = kwargs.get("redis_settings", settings.redis_settings)
        redis_pool: ArqRedis | None = kwargs.get("redis_pool", None)
        burst: bool = kwargs.get("burst", False)
        on_startup: StartupShutdown | None = kwargs.get("on_startup", on_startup)
        on_shutdown: StartupShutdown | None = kwargs.get("on_shutdown", on_shutdown)
        on_job_start: StartupShutdown | None = kwargs.get("on_job_start", None)
        on_job_end: StartupShutdown | None = kwargs.get("on_job_end", None)
        after_job_end: StartupShutdown | None = kwargs.get("after_job_end", None)
        handle_signals: bool = kwargs.get("handle_signals", True)
        job_completion_wait: int = kwargs.get("job_completion_wait", 0)
        max_jobs: int = kwargs.get("max_jobs", 20)
        job_timeout: SecondsTimedelta = kwargs.get("job_timeout", 300)
        keep_result: SecondsTimedelta = kwargs.get("keep_result", 30)
        keep_result_forever: bool = kwargs.get("keep_result_forever", False)
        poll_delay: SecondsTimedelta = kwargs.get("poll_delay", 0.5)
        queue_read_limit: int | None = kwargs.get("queue_read_limit", None)
        max_tries: int = kwargs.get("max_tries", 5)
        health_check_interval: SecondsTimedelta = kwargs.get("health_check_interval", 60)
        health_check_key: str | None = kwargs.get("health_check_key", settings.health_check_key)
        ctx: dict[Any, Any] | None = kwargs.get("ctx", None)
        retry_jobs: bool = kwargs.get("retry_jobs", False)
        allow_abort_jobs: bool = kwargs.get("allow_abort_jobs", True)
        max_burst_jobs: int = kwargs.get("max_burst_jobs", -1)
        job_serializer: Serializer = kwargs.get("job_serializer", settings.serializer)
        job_deserializer: Deserializer = kwargs.get("job_deserializer", settings.deserializer)
        expires_extra_ms: int = kwargs.get("expires_extra_ms", 86400000)
        timezone: datetime.timezone | None = kwargs.get("timezone", None)
        log_results: bool = kwargs.get("log_results", True)

    return Settings
