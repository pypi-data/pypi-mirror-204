from __future__ import annotations

__all__ = ["QueueSettings"]

from typing import Callable
from dataclasses import dataclass
from arq.connections import RedisSettings

from .serializers import serializer, deserializer


@dataclass
class QueueSettings:
    """Settings class used to hold configuration used by the worker(s) and for communicating with the queue."""

    redis_host: str
    redis_port: int = 6379
    redis_username: str | None = None
    redis_password: str | None = None

    queue_name: str = "pool:queue"
    health_check_key: str = "pool:queue:health"

    serializer: Callable = serializer
    deserializer: Callable = deserializer

    @property
    def redis_settings(self) -> RedisSettings:
        return RedisSettings(
            host=self.redis_host,
            port=self.redis_port,
            username=self.redis_username,
            password=self.redis_password,
            conn_timeout=10,
        )
