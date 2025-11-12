from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass
class EncryptedPayload:
    ciphertext: bytes
    nonce: bytes
    key: bytes
    key_digest: str
    payload_hash: str

    def as_transport_dict(self) -> dict[str, str]:
        return {
            "ciphertext": base64.b64encode(self.ciphertext).decode("utf-8"),
            "nonce": base64.b64encode(self.nonce).decode("utf-8"),
            "key": base64.b64encode(self.key).decode("utf-8"),
            "key_digest": self.key_digest,
            "payload_hash": self.payload_hash,
        }


class EncryptionService:
    def __init__(self, key_size: int = 32) -> None:
        if key_size not in (16, 24, 32):
            raise ValueError("key_size must be 16, 24 or 32 bytes for AES-GCM")
        self._key_size = key_size

    def encrypt(self, data: bytes) -> EncryptedPayload:
        key = os.urandom(self._key_size)
        nonce = os.urandom(12)
        aes = AESGCM(key)
        ciphertext = aes.encrypt(nonce, data, None)

        key_digest = hashlib.sha256(key).hexdigest()
        payload_hash = hashlib.sha256(ciphertext).hexdigest()

        return EncryptedPayload(
            ciphertext=ciphertext,
            nonce=nonce,
            key=key,
            key_digest=key_digest,
            payload_hash=payload_hash,
        )

    def decrypt(self, payload: EncryptedPayload) -> bytes:
        aes = AESGCM(payload.key)
        return aes.decrypt(payload.nonce, payload.ciphertext, None)
