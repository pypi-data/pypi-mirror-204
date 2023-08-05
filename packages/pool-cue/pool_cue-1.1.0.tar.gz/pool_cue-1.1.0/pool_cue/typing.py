from __future__ import annotations

__all__ = ["GenerateJobIdFunction", "AsyncGenerateJobIdFunction", "PushJobFunction"]

from typing import Protocol
from arq.connections import ArqRedis


class GenerateJobIdFunction(Protocol):
    __qualname__: str

    def __call__(self, _func: str, _children: list[str] | None = None, **kwargs) -> str:
        pass


class AsyncGenerateJobIdFunction(Protocol):
    __qualname__: str

    async def __call__(self, _func: str, _children: list[str] | None = None, **kwargs) -> str:
        pass


class PushJobFunction(Protocol):
    __qualname__: str

    async def __call__(
        self,
        _redis: ArqRedis,
        _func: str,
        _job_id: str | GenerateJobIdFunction | AsyncGenerateJobIdFunction | None = None,
        _children: list[str] | None = None,
        _delay: tuple[int, int] | None = None,
        _force: bool = False,
        _queue_name: str | None = None,
        **kwargs,
    ) -> None:
        pass
