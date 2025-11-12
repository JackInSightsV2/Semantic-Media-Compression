from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ...services.crypto import EncryptedPayload


@dataclass
class IPFSUploadResult:
    cid: str
    proof: str
    metadata: dict[str, str]


class IPFSClient(Protocol):
    async def upload_encrypted(self, payload: EncryptedPayload) -> IPFSUploadResult: ...

    async def upload_plaintext(self, data: bytes) -> IPFSUploadResult: ...
    
    async def upload_json(self, data: dict[str, Any]) -> IPFSUploadResult: ...