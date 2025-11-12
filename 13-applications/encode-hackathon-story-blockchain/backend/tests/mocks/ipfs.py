from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from backend.adapters.ipfs.base import IPFSClient, IPFSUploadResult
from backend.services.crypto import EncryptedPayload


@dataclass
class MockIPFSClient(IPFSClient):
    """
    Test double for IPFS interactions.

    Features:
    - Stores uploaded payloads in-memory keyed by deterministic SHA-256 “cid”.
    - Supports both encrypted and plaintext uploads.
    - Optional failure injection via ``raise_on_upload``.
    """

    raise_on_upload: bool = False
    _storage: Dict[str, bytes] = field(default_factory=dict)
    _metadata: Dict[str, dict[str, str]] = field(default_factory=dict)

    async def upload_encrypted(self, payload: EncryptedPayload) -> IPFSUploadResult:
        if self.raise_on_upload:
            raise RuntimeError("Mock IPFS failure (encrypted)")

        cid_bytes = payload.ciphertext + payload.nonce
        cid = hashlib.sha256(cid_bytes).hexdigest()
        self._storage[cid] = payload.ciphertext
        metadata = {
            "nonce": payload.nonce.hex(),
            "key_digest": payload.key_digest,
            "mode": "encrypted",
        }
        self._metadata[cid] = metadata
        return IPFSUploadResult(cid=cid, proof=payload.payload_hash, metadata=metadata)

    async def upload_plaintext(self, data: bytes) -> IPFSUploadResult:
        if self.raise_on_upload:
            raise RuntimeError("Mock IPFS failure (plaintext)")

        cid = hashlib.sha256(data).hexdigest()
        proof = hashlib.sha256(data).hexdigest()
        metadata = {"mode": "plaintext"}
        self._storage[cid] = data
        self._metadata[cid] = metadata
        return IPFSUploadResult(cid=cid, proof=proof, metadata=metadata)

    async def upload_json(self, data: dict[str, Any]) -> IPFSUploadResult:
        """Upload a JSON dictionary as plaintext to IPFS."""
        json_bytes = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return await self.upload_plaintext(json_bytes)

    def get_blob(self, cid: str) -> bytes:
        return self._storage[cid]

    def get_metadata(self, cid: str) -> Optional[dict[str, str]]:
        return self._metadata.get(cid)
