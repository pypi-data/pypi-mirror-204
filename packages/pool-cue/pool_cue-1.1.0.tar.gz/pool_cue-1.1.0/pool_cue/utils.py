from __future__ import annotations

__all__ = ["get_tasks", "generate_job_id"]


from typing import Sequence
from types import ModuleType
from inspect import getmembers, isfunction
from arq.worker import Function
from arq.typing import WorkerCoroutine


def get_tasks(modules: ModuleType | Sequence[ModuleType]) -> Sequence[Function | WorkerCoroutine]:
    """
    Returns every callable from the given module (or list of modules).
    """
    return (
        [func for module in modules for _, func in getmembers(module, isfunction)]
        if isinstance(modules, list)
        else [func for _, func in getmembers(modules, isfunction)]
    )


def generate_job_id(_func: str, _children: list[str] | None = None, **kwargs) -> str:
    """
    Generate a 'unique' job identifier from the given arguments.
    """
    suffix: str = "_parent_job" if _children else "_job"
    _hash: str = f"_{abs(hash(frozenset(kwargs.items())))}" if kwargs else ""
    return _func + suffix + _hash
