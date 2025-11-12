from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(slots=True)
class NotificationMessage:
    recipient: str
    channels: list[str]
    payload: dict


class NotificationDispatcher(Protocol):
    async def dispatch(self, message: NotificationMessage) -> None: ...


@dataclass
class InMemoryNotificationDispatcher(NotificationDispatcher):
    messages: list[NotificationMessage] = field(default_factory=list)

    async def dispatch(self, message: NotificationMessage) -> None:
        self.messages.append(message)
