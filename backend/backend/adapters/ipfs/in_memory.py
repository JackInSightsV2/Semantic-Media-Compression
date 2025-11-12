from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from typing import Dict

from ...services.crypto import EncryptedPayload
from .base import IPFSClient, IPFSUploadResult


@dataclass
class InMemoryIPFSClient(IPFSClient):
    _storage: Dict[str, bytes] = field(default_factory=dict)

    async def upload_encrypted(self, payload: EncryptedPayload) -> IPFSUploadResult:
        cid_source = payload.ciphertext + payload.nonce
        cid = hashlib.sha256(cid_source).hexdigest()
        self._storage[cid] = payload.ciphertext

        metadata = {
            "nonce": base64.b64encode(payload.nonce).decode("utf-8"),
            "key_digest": payload.key_digest,
        }

        return IPFSUploadResult(
            cid=cid,
            proof=payload.payload_hash,
            metadata=metadata,
        )

    def fetch_ciphertext(self, cid: str) -> bytes:
        return self._storage[cid]
