from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ...services.crypto import EncryptedPayload


@dataclass
class IPFSUploadResult:
    cid: str
    proof: str
    metadata: dict[str, str]


class IPFSClient(Protocol):
    async def upload_encrypted(self, payload: EncryptedPayload) -> IPFSUploadResult: ...
