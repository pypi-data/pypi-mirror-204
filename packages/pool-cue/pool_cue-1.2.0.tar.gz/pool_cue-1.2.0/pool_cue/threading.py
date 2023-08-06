from __future__ import annotations

__all__ = ["run_in_thread_pool"]

import asyncio
import functools
import threading
import logging
from typing import Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor

from .context import Context

logger: logging.Logger = logging.getLogger(name="pool_cue")

THREAD_POOL_EVENT_LOOPS: dict[int, asyncio.AbstractEventLoop] = {}


def _run_coro_in_thread_pool(_coro: Callable, *args, **kwargs) -> None:
    """
    Function used by 'run_in_thread_pool' to support running asynchronous functions in sub-threads:
    Creates a new event loop in the current (sub-)thread (if one doesn't already exist)
    to make it possible to call async functions.

    Based on:
    https://stackoverflow.com/questions/46074841/why-coroutines-cannot-be-used-with-run-in-executor/63106889#63106889
    """
    current_thread_id: int = threading.current_thread().ident
    global THREAD_POOL_EVENT_LOOPS
    if current_thread_id not in THREAD_POOL_EVENT_LOOPS:
        logger.debug("Creating new event loop in sub-thread %s...", current_thread_id)
        THREAD_POOL_EVENT_LOOPS[current_thread_id] = asyncio.new_event_loop()
    loop: asyncio.AbstractEventLoop = THREAD_POOL_EVENT_LOOPS[current_thread_id]
    future: Coroutine = _coro(*args, **kwargs)
    try:
        loop.run_until_complete(future=future)
    except Exception as exc:
        logger.warning(
            "An error occurred while running coroutine '%s' in sub-thread %s!",
            str(_coro),
            current_thread_id,
            exc_info=exc,
        )


async def run_in_thread_pool(_ctx: Context, _func: Callable, *args, **kwargs) -> None:
    """
    Run the given function in the queue worker's dedicated thread pool.
    Use this to run I/O bound tasks without blocking the worker's main thread.

    Supports both synchronous and asynchronous functions.

    :param _ctx: The worker context.
    :param _func: The function to run in a sub-thread.
    :param args: Positional arguments to pass to the function.
    :param kwargs: Keyword arguments to pass to the function.
    """
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    pool: ThreadPoolExecutor = _ctx["pool"]
    if asyncio.iscoroutinefunction(func=_func):
        try:
            await loop.run_in_executor(
                executor=pool, func=functools.partial(_run_coro_in_thread_pool, _coro=_func, *args, **kwargs)
            )
        except Exception as exc:
            logger.warning("Failed to run coroutine in thread pool executor!", exc_info=exc)
    else:
        try:
            await loop.run_in_executor(executor=pool, func=functools.partial(_func, *args, **kwargs))
        except Exception as exc:
            logger.warning("Failed to run function in thread pool executor!", exc_info=exc)
