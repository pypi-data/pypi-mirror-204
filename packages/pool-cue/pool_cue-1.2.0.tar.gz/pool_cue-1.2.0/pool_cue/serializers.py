from __future__ import annotations

__all__ = ["deserializer", "serializer"]

from typing import Any
import msgpack
import logging

logger: logging.Logger = logging.getLogger(name="pool_cue")


def serializer(o: Any, **kwargs: Any) -> bytes | None:
    """
    Msgpack job serializer.
    """
    try:
        return msgpack.packb(o=o, **kwargs)
    except Exception as exc:
        logger.warning("Failed to serialize data!", exc_info=exc)


def deserializer(b: bytes) -> Any | None:
    """
    Msgpack job deserializer.
    """
    try:
        return msgpack.unpackb(packed=b, raw=False)
    except Exception as exc:
        logger.warning("Failed to deserialize data!", exc_info=exc)
