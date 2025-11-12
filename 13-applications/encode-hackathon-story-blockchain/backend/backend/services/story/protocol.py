from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid5

try:
    from story_protocol_python_sdk import StoryClient
    from web3 import Web3

    STORY_SDK_AVAILABLE = True
except ImportError:
    STORY_SDK_AVAILABLE = False
    Web3 = None  # type: ignore


@dataclass
class StoryRegistrationResult:
    ip_asset_id: str
    token_id: str
    tx_hash: str


@dataclass
class StoryViolationReport:
    tx_hash: str
    content_hash: str
    infringing_url: str | None
    evidence_hash: str


class StoryProtocolClient(Protocol):
    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict[str, Any],
    ) -> StoryRegistrationResult: ...

    async def report_violation(
        self,
        *,
        content_hash: str,
        infringing_url: str | None,
        evidence_hash: str,
    ) -> StoryViolationReport: ...


@dataclass
class MockStoryProtocolClient(StoryProtocolClient):
    namespace: UUID
    reports: list[StoryViolationReport] = field(default_factory=list)

    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict[str, Any],
    ) -> StoryRegistrationResult:
        seed = f"{asset_id}:{cid}:{proof}".encode("utf-8")
        ip_asset_uuid = uuid5(self.namespace, seed.hex())
        token_uuid = uuid5(self.namespace, hashlib.sha256(seed).hexdigest())
        tx_hash = hashlib.sha256(seed + b"tx").hexdigest()

        return StoryRegistrationResult(
            ip_asset_id=str(ip_asset_uuid),
            token_id=str(token_uuid),
            tx_hash=f"0x{tx_hash[:64]}",
        )

    async def report_violation(
        self,
        *,
        content_hash: str,
        infringing_url: str | None,
        evidence_hash: str,
    ) -> StoryViolationReport:
        seed = f"{content_hash}:{infringing_url}:{evidence_hash}".encode("utf-8")
        tx_hash = hashlib.sha256(seed).hexdigest()
        report = StoryViolationReport(
            tx_hash=f"0x{tx_hash[:64]}",
            content_hash=content_hash,
            infringing_url=infringing_url,
            evidence_hash=evidence_hash,
        )
        self.reports.append(report)
        return report


@dataclass
class RealStoryProtocolClient(StoryProtocolClient):
    """
    Real Story Protocol client implementation using the official Python SDK.

    Requires:
    - STORY_WALLET_PRIVATE_KEY: Private key for the wallet (without 0x prefix)
    - STORY_RPC_PROVIDER_URL: RPC provider URL (defaults to Aeneid testnet)
    - STORY_CHAIN_ID: Chain ID (1315 for Aeneid testnet, 1514 for mainnet)
    - STORY_SPG_NFT_CONTRACT: Optional SPG NFT contract address for minting
    """

    wallet_private_key: str
    rpc_provider_url: str
    chain_id: int
    spg_nft_contract: str | None = None
    _client: Any | None = field(default=None, init=False, repr=False)
    _web3: Any | None = field(default=None, init=False, repr=False)
    _account: Any | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if not STORY_SDK_AVAILABLE:
            raise ImportError(
                "story-protocol-python-sdk is not installed. "
                "Install it with: pip install story-protocol-python-sdk web3"
            )

        if Web3 is None:
            raise ImportError("web3 library is required but not installed")

        # Initialize Web3
        self._web3 = Web3(Web3.HTTPProvider(self.rpc_provider_url))
        if not self._web3.is_connected():
            raise ConnectionError(f"Failed to connect to RPC provider: {self.rpc_provider_url}")

        # Create account from private key
        private_key_hex = (
            self.wallet_private_key
            if self.wallet_private_key.startswith("0x")
            else f"0x{self.wallet_private_key}"
        )
        self._account = self._web3.eth.account.from_key(private_key_hex)

        # Initialize Story Client
        self._client = StoryClient(self._web3, self._account, self.chain_id)

    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict[str, Any],
    ) -> StoryRegistrationResult:
        """
        Register an asset on Story Protocol by minting a new NFT and registering it as an IP Asset.

        Args:
            asset_id: Internal asset identifier
            cid: IPFS CID of the content
            proof: Cryptographic proof (zk_proof)
            metadata: Additional metadata for the IP asset

        Returns:
            StoryRegistrationResult with ip_asset_id, token_id, and tx_hash
        """
        if self._client is None:
            raise RuntimeError("Story client not initialized")

        # Build IP metadata from CID and proof
        # IPFS gateway URL for the metadata
        ip_metadata_uri = f"https://ipfs.io/ipfs/{cid}"
        nft_metadata_uri = ip_metadata_uri  # Can be the same or different

        # Create metadata hash from proof and CID
        # The proof is used as the hash for verification
        proof_hash = proof if proof.startswith("0x") else f"0x{proof}"

        # If proof is not a valid hex hash, create one from the proof string
        try:
            # Try to validate it's a hex string
            int(proof_hash, 16)
            ip_metadata_hash = proof_hash
        except ValueError:
            # If not valid hex, create a hash from the proof
            proof_bytes = proof.encode("utf-8") if isinstance(proof, str) else proof
            ip_metadata_hash = Web3.to_hex(Web3.keccak(proof_bytes))

        # Use the same hash for NFT metadata or create a separate one
        nft_metadata_hash = ip_metadata_hash

        # Prepare IP metadata
        ip_metadata = {
            "ip_metadata_uri": ip_metadata_uri,
            "ip_metadata_hash": ip_metadata_hash,
            "nft_metadata_uri": nft_metadata_uri,
            "nft_metadata_hash": nft_metadata_hash,
        }

        # Use default SPG contract if not provided
        # Default SPG contract for Aeneid testnet
        default_spg_contract = "0xc32A8a0FF3beDDDa58393d022aF433e78739FAbc"
        spg_contract = self.spg_nft_contract or default_spg_contract

        try:
            # Register IP Asset by minting a new NFT
            response = self._client.IPAsset.register(
                nft_contract=spg_contract,
                token_id=None,  # None means mint a new NFT
                ip_metadata=ip_metadata,
                tx_options={"wait_for_transaction": True},
            )

            # Extract results from response
            ip_id = response.get("ip_id") or response.get("ipId")
            tx_hash = response.get("tx_hash") or response.get("txHash")
            token_id = response.get("token_id") or response.get("tokenId")

            if not ip_id or not tx_hash:
                raise ValueError(f"Invalid response from Story Protocol: {response}")

            return StoryRegistrationResult(
                ip_asset_id=str(ip_id),
                token_id=str(token_id) if token_id else "0",  # Token ID may not be returned
                tx_hash=str(tx_hash),
            )
        except Exception as e:
            raise RuntimeError(f"Failed to register asset on Story Protocol: {e}") from e

    async def report_violation(
        self,
        *,
        content_hash: str,
        infringing_url: str | None,
        evidence_hash: str,
    ) -> StoryViolationReport:
        """
        Report a violation to Story Protocol.

        Note: The Story Protocol Python SDK may not have a direct violation reporting method.
        This implementation logs the violation data. You may need to implement custom logic
        or use the protocol's dispute/claim mechanisms.

        Args:
            content_hash: Hash of the original content
            infringing_url: URL where the infringement was detected
            evidence_hash: Hash of the evidence

        Returns:
            StoryViolationReport with tx_hash
        """
        if self._client is None:
            raise RuntimeError("Story client not initialized")

        # Note: Story Protocol SDK may not have a direct violation reporting endpoint
        # This is a placeholder implementation. You may need to:
        # 1. Use the dispute/claim system
        # 2. Register the violation as metadata
        # 3. Use a custom smart contract interaction

        # For now, we'll create a hash-based transaction ID
        if Web3 is None:
            raise RuntimeError("Web3 not available")
        violation_data = f"{content_hash}:{infringing_url}:{evidence_hash}".encode("utf-8")
        tx_hash = Web3.to_hex(Web3.keccak(violation_data))

        # TODO: Implement actual violation reporting when Story Protocol SDK supports it
        # or implement custom smart contract interaction

        return StoryViolationReport(
            tx_hash=tx_hash,
            content_hash=content_hash,
            infringing_url=infringing_url,
            evidence_hash=evidence_hash,
        )
