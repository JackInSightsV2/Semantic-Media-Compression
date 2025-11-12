from __future__ import annotations

from typing import Awaitable, Callable, Protocol
from uuid import UUID

TaskHandler = Callable[[dict], Awaitable[None]]


class TaskDispatcher(Protocol):
    async def register(self, name: str, handler: TaskHandler) -> None: ...

    async def dispatch(self, name: str, payload: dict) -> UUID: ...
