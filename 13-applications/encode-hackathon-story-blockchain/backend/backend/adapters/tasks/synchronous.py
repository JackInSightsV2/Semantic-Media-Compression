from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID, uuid4

from .base import TaskDispatcher, TaskHandler


@dataclass
class SynchronousTaskDispatcher(TaskDispatcher):
    """
    Simple in-process task dispatcher used for local development and testing.
    Registered handlers are awaited immediately when dispatched.
    """

    _handlers: Dict[str, TaskHandler] = field(default_factory=dict)

    async def register(self, name: str, handler: TaskHandler) -> None:
        self._handlers[name] = handler

    async def dispatch(self, name: str, payload: dict) -> UUID:
        job_id = uuid4()
        handler = self._handlers.get(name)
        if handler is None:
            raise ValueError(f"No handler registered for task '{name}'")
        await handler(payload)
        return job_id
