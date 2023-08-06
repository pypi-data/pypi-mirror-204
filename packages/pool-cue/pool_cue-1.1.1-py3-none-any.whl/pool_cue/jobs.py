from __future__ import annotations

__all__ = ["get_jobs", "push_job"]

import logging
import asyncio
from typing import Callable
from random import randint
from arq.jobs import JobDef
from arq.connections import ArqRedis

from .exceptions import QueueError
from .utils import generate_job_id
from .typing import GenerateJobIdFunction, AsyncGenerateJobIdFunction

logger: logging.Logger = logging.getLogger(name="pool_cue")


async def get_jobs(redis: ArqRedis, queue_name: str | None = None) -> list[JobDef]:
    """
    Get all jobs that are currently in the given redis queue (queued or running).

    :param redis: Redis queue connection.
    :param queue_name: Redis queue name.
        The default queue name from the Redis connection will be used if not specified.
    """
    _queue_name: str = queue_name or redis.default_queue_name
    try:
        jobs: list[JobDef] = await redis.queued_jobs(queue_name=_queue_name)
    except (AssertionError, TimeoutError) as exc:
        logger.warning("Failed to get queued jobs from '%s'!", _queue_name, exc_info=exc)
        raise QueueError("Failed to get queued jobs") from exc
    except Exception as exc:
        logger.error("Failed to get queued jobs from '%s'!", _queue_name, exc_info=exc)
        raise QueueError("Failed to get queued jobs") from exc
    else:
        return jobs


async def _job_already_exists(
    _redis: ArqRedis, _func: str, _children: list[str] | None = None, _queue_name: str | None = None, **kwargs
) -> bool:
    """
    Check if a job with the given arguments already exists in the queue (queued or running).

    Returns True if:

    - A job with the same function name and keyword arguments (if any) is found.
    - A job whose function name matches any of the names specified using the '_children' argument is found.

    :param _redis: Redis queue connection.
    :param _func: Job function name.
    :param _children: Optional list of other job function names.
    :param _queue_name: Redis queue name.
        The default queue name from the Redis connection will be used if not specified.
    :param kwargs: Optional job function keyword arguments.
        Used together with the function name to find matching jobs in the queue.
    :return: Boolean indicating whether the job (or its children) already exists in the queue.
    """
    try:
        jobs: list[JobDef] = await get_jobs(redis=_redis, queue_name=_queue_name)
    except QueueError as exc:
        logger.warning("Failed to check if job '%s' already exists in the queue!", _func, exc_info=exc)
        return True  # return True to keep new jobs from being queued if an error occurs
    if not _children:
        return (
            any(job.function == _func and job.kwargs == kwargs for job in jobs)
            if kwargs
            else any(job.function == _func for job in jobs)
        )
    return (
        any((job.function == _func and job.kwargs == kwargs) or job.function in _children for job in jobs)
        if kwargs
        else any(job.function == _func or job.function in _children for job in jobs)
    )


async def push_job(
    _redis: ArqRedis,
    _func: str,
    _job_id: str | GenerateJobIdFunction | AsyncGenerateJobIdFunction | None = generate_job_id,
    _children: list[str] | None = None,
    _delay: tuple[int, int] | None = None,
    _force: bool = False,
    _queue_name: str | None = None,
    **kwargs,
) -> None:
    """
    Push a new job to the queue.

    By default, a job will not be added to the queue if it (or any of its children) already exists in the queue.
    This behaviour cam be controlled using the '_children' and '_force' keyword arguments.

    :param _redis: Redis queue connection.
    :param _func: Job function name.
    :param _job_id: Optional job ID used by arq to enforce job uniqueness.
        By default, the job will be given an ID based on its function name, children, and keyword arguments.
    :param _children: Optional list of other job function names.
        Used to stop jobs that spawn child jobs from being queued as long as any of its children remain in the queue.
    :param _delay: Duration (in seconds) to wait before running the job.
        The duration will be chosen randomly from within the given range.
    :param _force: If True, the job will be added to the queue even if it or its children already exist in the queue.
        Combine with the '_job_id' argument to skip enforcing job uniqueness.
    :param _queue_name: Redis queue name.
        The default queue name from the Redis connection will be used if not specified.
    :param kwargs: Keyword arguments to pass to the job function.
    """
    _id: str | None
    if isinstance(_job_id, Callable):
        _id = (
            await _job_id(_func=_func, _children=_children, **kwargs)
            if asyncio.iscoroutinefunction(func=_job_id)
            else _job_id(_func=_func, _children=_children, **kwargs)
        )
    else:
        _id = _job_id
    if not _force:
        if await _job_already_exists(
            _redis=_redis, _func=_func, _children=_children, _queue_name=_queue_name, **kwargs
        ):
            logger.warning("Job '%s' is already queued!", _id or _func)
            return
    _defer_by: int | None = randint(a=_delay[0], b=_delay[1]) if _delay else None
    logger.debug("Adding job '%s' to the queue...", _id or _func)
    try:
        await _redis.enqueue_job(
            function=_func,
            _job_id=_id,
            _queue_name=_queue_name or _redis.default_queue_name,
            _defer_by=_defer_by,
            **kwargs,
        )
    except Exception as exc:
        logger.error("Failed to add job '%s' to the queue!", _id or _func, exc_info=exc)
