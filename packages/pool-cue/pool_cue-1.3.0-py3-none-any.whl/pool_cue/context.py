from __future__ import annotations

__all__ = ["Context", "init_context", "close_context"]

import datetime
import asyncio
import uvloop
import logging
import threading
from typing import TypedDict
from concurrent.futures import ThreadPoolExecutor
from arq.connections import ArqRedis

from .typing import QueueFunction
from .jobs import push_job

logger: logging.Logger = logging.getLogger(name="pool_cue")


class Context(TypedDict):
    redis: ArqRedis
    job_id: str
    job_try: int
    enqueue_time: datetime.datetime
    score: float

    # custom
    pool: ThreadPoolExecutor
    lock: threading.Lock
    queue_fn: QueueFunction


def _thread_pool_initializer(*args) -> None:
    logger.debug("Initializing new worker thread...")
    asyncio.set_event_loop_policy(policy=uvloop.EventLoopPolicy())


async def init_context(ctx: Context, thread_name_prefix: str = "SubThread", max_workers: int | None = None) -> Context:
    """
    Initialize a new thread pool executor in the given worker context.
    """
    ctx["pool"] = ThreadPoolExecutor(
        thread_name_prefix=thread_name_prefix, max_workers=max_workers, initializer=_thread_pool_initializer
    )
    ctx["lock"] = threading.Lock()
    ctx["queue_fn"] = push_job
    return ctx


async def close_context(ctx: Context) -> None:
    """
    Shut down the thread pool executor in the given worker context.
    """
    pool: ThreadPoolExecutor = ctx["pool"]
    pool.shutdown(wait=False, cancel_futures=True)
