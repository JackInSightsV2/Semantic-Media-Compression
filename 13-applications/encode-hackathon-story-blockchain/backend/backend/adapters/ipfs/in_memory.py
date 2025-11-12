from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict

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
            "mode": "encrypted",
        }

        return IPFSUploadResult(
            cid=cid,
            proof=payload.payload_hash,
            metadata=metadata,
        )

    async def upload_plaintext(self, data: bytes) -> IPFSUploadResult:
        cid = hashlib.sha256(data).hexdigest()
        self._storage[cid] = data
        metadata = {
            "mode": "plaintext",
        }
        return IPFSUploadResult(
            cid=cid,
            proof=hashlib.sha256(data).hexdigest(),
            metadata=metadata,
        )

    async def upload_json(self, data: dict[str, Any]) -> IPFSUploadResult:
        """Upload a JSON dictionary as plaintext to IPFS."""
        json_bytes = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return await self.upload_plaintext(json_bytes)

    def fetch_content(self, cid: str) -> bytes:
        return self._storage[cid]
