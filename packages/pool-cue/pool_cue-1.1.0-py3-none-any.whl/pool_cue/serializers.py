from __future__ import annotations

__all__ = ["deserializer", "serializer"]

from typing import Callable, Any
import msgpack


serializer: Callable = msgpack.packb


def deserializer(b: bytes) -> Any:
    """
    Msgpack job deserializer, works the same as:

    >>> lambda b: msgpack.unpackb(packed=b, raw=False)

    :param b: Bytes.
    :return: Deserialized bytes.
    """
    return msgpack.unpackb(packed=b, raw=False)
