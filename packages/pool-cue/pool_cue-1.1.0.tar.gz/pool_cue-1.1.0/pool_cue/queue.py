from __future__ import annotations

__all__ = ["Queue"]

import logging
from typing import Self
from arq.connections import ArqRedis, create_pool
from arq.jobs import JobDef

from .config import QueueSettings
from .exceptions import QueueError
from .utils import generate_job_id
from .jobs import push_job, get_jobs
from .typing import GenerateJobIdFunction, AsyncGenerateJobIdFunction


logger: logging.Logger = logging.getLogger(name="pool_cue")


class Queue:
    """Class used to interact with the worker(s)/ queue through Redis."""

    redis: ArqRedis

    def __init__(self, settings: QueueSettings) -> None:
        self.settings: QueueSettings = settings
        self.redis: ArqRedis | None = None

    async def connect(self) -> None:
        """Establish a new connection to the Redis queue (if one does not already exist)."""
        if not self.redis:
            self.redis = await create_pool(
                settings_=self.settings.redis_settings,
                job_serializer=self.settings.serializer,
                job_deserializer=self.settings.deserializer,
                default_queue_name=self.settings.queue_name,
            )

    async def disconnect(self) -> None:
        """Close the connection to the Redis queue (if it exists)."""
        if self.redis:
            await self.redis.close(close_connection_pool=True)

    async def _assert_redis_connection(self) -> None:
        if not self.redis:
            raise QueueError("Redis connection has not been established!")

    async def get_jobs(self) -> list[JobDef]:
        """Get all jobs that are currently in the queue (queued or running)."""
        await self._assert_redis_connection()
        return await get_jobs(redis=self.redis, queue_name=self.settings.queue_name)

    async def push_job(
        self,
        _func: str,
        _job_id: str | GenerateJobIdFunction | AsyncGenerateJobIdFunction | None = generate_job_id,
        _children: list[str] | None = None,
        _delay: tuple[int, int] | None = None,
        _force: bool = False,
        **kwargs,
    ) -> None:
        """
        Push a new job to the queue.

        By default, a job will not be added to the queue if it (or any of its children) already exists in the queue.
        This behaviour cam be controlled using the '_children' and '_force' keyword arguments.

        :param _func: Job function name.
        :param _job_id: Optional job ID used by arq to enforce job uniqueness.
        :param _children: Optional list of other job function names.
            Used to stop new 'parent jobs' from being queued as long as any of its children remain in the queue.
        :param _delay: Duration (in seconds) to wait before running the job.
        :param _force: If True, the job will be added to the queue even if it
            or its children already exist in the queue.
        :param kwargs: Keyword arguments to pass to the job function.
        """
        await self._assert_redis_connection()
        return await push_job(
            _redis=self.redis,
            _func=_func,
            _job_id=_job_id,
            _children=_children,
            _delay=_delay,
            _force=_force,
            _queue_name=self.settings.queue_name,
            **kwargs,
        )

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.disconnect()
