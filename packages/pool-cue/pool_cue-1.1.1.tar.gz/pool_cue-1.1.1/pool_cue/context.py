from __future__ import annotations

__all__ = ["Context", "init_context", "close_context"]

import datetime
from typing import TypedDict
from concurrent.futures import ThreadPoolExecutor
from arq.connections import ArqRedis

from .typing import PushJobFunction
from .jobs import push_job


class Context(TypedDict):
    redis: ArqRedis
    job_id: str
    job_try: int
    enqueue_time: datetime.datetime
    score: float

    # custom
    pool: ThreadPoolExecutor
    push_job_fn: PushJobFunction


async def init_context(ctx: Context, thread_name_prefix: str = "SubThread", max_workers: int | None = None) -> Context:
    """
    Initialize a new thread pool executor in the given worker context.
    """
    ctx["pool"] = ThreadPoolExecutor(thread_name_prefix=thread_name_prefix, max_workers=max_workers)
    ctx["push_job_fn"] = push_job
    return ctx


async def close_context(ctx: Context) -> None:
    """
    Shut down the thread pool executor in the given worker context.
    """
    pool: ThreadPoolExecutor = ctx["pool"]
    pool.shutdown()
