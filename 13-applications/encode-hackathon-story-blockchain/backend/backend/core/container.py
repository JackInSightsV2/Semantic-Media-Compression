from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from uuid import UUID

from ..adapters.ipfs.in_memory import InMemoryIPFSClient
from ..adapters.repositories.in_memory import (
    InMemoryAlertRepository,
    InMemoryContentRepository,
    InMemoryDisputeRepository,
    InMemoryEvidenceRepository,
    InMemoryIntegrationRepository,
    InMemoryJobRepository,
    InMemoryNotificationRepository,
    InMemoryScanRepository,
    InMemoryViolationRepository,
)
from ..adapters.storage.base import AssetStore
from ..adapters.storage.in_memory import InMemoryAssetStore
from ..adapters.tasks.base import TaskDispatcher
from ..adapters.tasks.synchronous import SynchronousTaskDispatcher
from ..modules.shared.repositories import RepositoryBundle
from ..modules.monitoring import MonitoringSettings
from ..services.crypto import EncryptionService
from ..services.embeddings import EmbeddingProvider, MockEmbeddingProvider
from ..services.external import InstagramClient, MockPlatformClient, PlatformClient, TikTokClient, YouTubeClient
from ..services.notifications import InMemoryNotificationDispatcher, NotificationDispatcher
from ..services.story.protocol import (
    MockStoryProtocolClient,
    RealStoryProtocolClient,
    StoryProtocolClient,
)
from ..services.vector_index import InMemoryVectorIndex, VectorIndex
from .logging import configure_logging
from .settings import (
    AppSettings,
    EmbeddingProviderProfile,
    Profile,
    StorageProfile,
    TaskDispatcherProfile,
    get_settings,
)


@dataclass
class RepositoryContainer(RepositoryBundle):
    content: InMemoryContentRepository
    scans: InMemoryScanRepository
    disputes: InMemoryDisputeRepository
    alerts: InMemoryAlertRepository
    jobs: InMemoryJobRepository
    integrations: InMemoryIntegrationRepository
    evidence: InMemoryEvidenceRepository
    violations: InMemoryViolationRepository
    notifications: InMemoryNotificationRepository


@dataclass
class AppContainer:
    settings: AppSettings
    repositories: RepositoryBundle
    asset_store: AssetStore
    task_dispatcher: TaskDispatcher
    embedding_provider: EmbeddingProvider
    encryption_service: EncryptionService
    ipfs_client: InMemoryIPFSClient
    story_client: StoryProtocolClient
    vector_index: VectorIndex
    platform_clients: dict[str, PlatformClient]
    monitoring_settings: MonitoringSettings
    notification_dispatcher: NotificationDispatcher


def _build_repositories(settings: AppSettings) -> RepositoryContainer:
    if settings.profile == Profile.LOCAL_DEV:
        return RepositoryContainer(
            content=InMemoryContentRepository(),
            scans=InMemoryScanRepository(),
            disputes=InMemoryDisputeRepository(),
            alerts=InMemoryAlertRepository(),
            jobs=InMemoryJobRepository(),
            integrations=InMemoryIntegrationRepository(),
            evidence=InMemoryEvidenceRepository(),
            violations=InMemoryViolationRepository(),
            notifications=InMemoryNotificationRepository(),
        )

    # TODO: Replace with SQL-backed repositories for production profiles.
    raise NotImplementedError(f"Repository provisioning not implemented for profile {settings.profile}")


def _build_asset_store(settings: AppSettings) -> AssetStore:
    if settings.storage_profile == StorageProfile.LOCAL:
        return InMemoryAssetStore()

    # TODO: Add Supabase/S3 implementations
    raise NotImplementedError(f"Asset store not implemented for profile {settings.storage_profile}")


def _build_task_dispatcher(settings: AppSettings) -> TaskDispatcher:
    if settings.task_profile == TaskDispatcherProfile.SYNC:
        return SynchronousTaskDispatcher()

    # TODO: Provide Celery-backed dispatcher
    raise NotImplementedError(f"Task dispatcher not implemented for profile {settings.task_profile}")


def _build_embedding_provider(settings: AppSettings) -> EmbeddingProvider:
    if settings.embedding_profile == EmbeddingProviderProfile.MOCK:
        return MockEmbeddingProvider()

    # TODO: Provide local-model and remote provider implementations
    raise NotImplementedError(f"Embedding provider not implemented for profile {settings.embedding_profile}")


def _build_platform_clients(settings: AppSettings) -> dict[str, PlatformClient]:
    external = settings.external
    clients: dict[str, PlatformClient] = {}

    if external.youtube_api_key:
        clients["youtube"] = YouTubeClient(api_key=external.youtube_api_key)
    else:
        clients["youtube"] = MockPlatformClient.from_pairs(
            "youtube",
            [
                ("Forest Journey", "A serene walk through the ancient forest with mist and quiet melodies."),
                ("Dreamscape Themes", "Exploration of dreamscapes and surreal storytelling elements."),
                ("Hackathon Stories", "Once upon a time in a hackathon with creative stories and innovative ideas."),
            ],
        )

    if external.instagram_access_token:
        clients["instagram"] = InstagramClient(access_token=external.instagram_access_token)
    else:
        clients["instagram"] = MockPlatformClient.from_pairs(
            "instagram",
            [
                ("Mist Morning", "Caption about misty forests and calm tones with dreamlike imagery."),
                ("Urban Fantasy", "Narrative blending city lights with enchanted woods."),
                ("Hackathon Time", "Creative hackathon project showcasing innovative storytelling techniques."),
            ],
        )

    if external.tiktok_api_key:
        clients["tiktok"] = TikTokClient(api_key=external.tiktok_api_key)
    else:
        clients["tiktok"] = MockPlatformClient.from_pairs(
            "tiktok",
            [
                ("Storytime", "Narration about growth and transformation in magical forests."),
                ("Ambient Beats", "Calm tempo audio clip describing serene moods."),
                ("Hackathon Creative", "Once upon a time we built something amazing at the hackathon event."),
            ],
        )

    return clients


def _build_story_client(settings: AppSettings) -> StoryProtocolClient:
    """
    Build Story Protocol client based on settings.
    
    Uses mock client if STORY_USE_MOCK is True or if wallet private key is not provided.
    Otherwise, uses the real Story Protocol Python SDK.
    """
    story_settings = settings.story

    # Use mock if explicitly configured or if private key is missing
    if story_settings.use_mock or not story_settings.wallet_private_key:
        return MockStoryProtocolClient(namespace=UUID("8a78d159-4f9d-4ec6-85d9-13d8f8f6c70d"))

    # Use real SDK client
    try:
        return RealStoryProtocolClient(
            wallet_private_key=story_settings.wallet_private_key,
            rpc_provider_url=story_settings.rpc_provider_url,
            chain_id=story_settings.chain_id,
            spg_nft_contract=story_settings.spg_nft_contract,
        )
    except ImportError as e:
        # Fall back to mock if SDK is not installed
        import warnings

        warnings.warn(
            f"Story Protocol Python SDK not available, using mock client: {e}",
            UserWarning,
        )
        return MockStoryProtocolClient(namespace=UUID("8a78d159-4f9d-4ec6-85d9-13d8f8f6c70d"))


@lru_cache()
def get_container() -> AppContainer:
    settings = get_settings()
    configure_logging(settings)

    repositories = _build_repositories(settings)
    asset_store = _build_asset_store(settings)
    dispatcher = _build_task_dispatcher(settings)
    embedding_provider = _build_embedding_provider(settings)
    encryption_service = EncryptionService()
    ipfs_client = InMemoryIPFSClient()
    story_client = _build_story_client(settings)
    vector_index: VectorIndex = InMemoryVectorIndex()
    platform_clients = _build_platform_clients(settings)
    monitoring_settings = MonitoringSettings()
    notification_dispatcher: NotificationDispatcher = InMemoryNotificationDispatcher()

    return AppContainer(
        settings=settings,
        repositories=repositories,
        asset_store=asset_store,
        task_dispatcher=dispatcher,
        embedding_provider=embedding_provider,
        encryption_service=encryption_service,
        ipfs_client=ipfs_client,
        story_client=story_client,
        vector_index=vector_index,
        platform_clients=platform_clients,
        monitoring_settings=monitoring_settings,
        notification_dispatcher=notification_dispatcher,
    )
