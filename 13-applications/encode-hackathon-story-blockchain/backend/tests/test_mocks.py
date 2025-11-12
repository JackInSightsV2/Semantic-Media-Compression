from __future__ import annotations

import pytest

from backend.services.crypto import EncryptionService
from tests.mocks.ipfs import MockIPFSClient
from tests.mocks.semantic import MockSemanticComparator
from tests.mocks.story import MockStoryProtocolClient


@pytest.mark.asyncio
async def test_mock_ipfs_handles_encrypted_and_plaintext() -> None:
    client = MockIPFSClient()
    encryption = EncryptionService()

    encrypted_payload = encryption.encrypt(b"super secret manuscript")
    encrypted_result = await client.upload_encrypted(encrypted_payload)
    assert encrypted_result.metadata["mode"] == "encrypted"
    assert client.get_blob(encrypted_result.cid) != b"super secret manuscript"

    plain_result = await client.upload_plaintext(b"public domain excerpt")
    assert plain_result.metadata["mode"] == "plaintext"
    assert client.get_blob(plain_result.cid) == b"public domain excerpt"


@pytest.mark.asyncio
async def test_mock_story_protocol_records_submissions(uuid_sequence) -> None:
    client = MockStoryProtocolClient(prefix="unit")
    asset_id = next(uuid_sequence)
    result = await client.register_asset(asset_id=asset_id, cid="cid123", proof="proof456", metadata={"chain": "test"})

    assert result.ip_asset_id.startswith("unit-ip-")
    assert result.token_id.startswith("unit-token-")
    assert client.get_registration(asset_id) == result


@pytest.mark.asyncio
async def test_mock_semantic_comparator_overrides() -> None:
    comparator = MockSemanticComparator(default_score=0.1)
    comparator.overrides[("0.100,0.200", "0.100,0.200")] = 0.99

    score_same = await comparator.compare([0.1, 0.2], [0.1, 0.2])
    score_diff = await comparator.compare([0.1, 0.2], [0.3, 0.4])

    assert score_same == pytest.approx(0.99)
    assert score_diff == pytest.approx(0.1)


@pytest.fixture
def uuid_sequence():
    import uuid

    def _generator():
        while True:
            yield uuid.uuid4()

    gen = _generator()
    return gen
