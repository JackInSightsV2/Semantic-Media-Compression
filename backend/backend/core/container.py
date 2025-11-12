from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..adapters.repositories.in_memory import (
    InMemoryAlertRepository,
    InMemoryContentRepository,
    InMemoryDisputeRepository,
    InMemoryIntegrationRepository,
    InMemoryJobRepository,
    InMemoryScanRepository,
)
from ..adapters.storage.base import AssetStore
from ..adapters.storage.in_memory import InMemoryAssetStore
from ..adapters.tasks.base import TaskDispatcher
from ..adapters.tasks.synchronous import SynchronousTaskDispatcher
from ..modules.shared.repositories import RepositoryBundle
from ..services.embeddings import EmbeddingProvider, MockEmbeddingProvider
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


@dataclass
class AppContainer:
    settings: AppSettings
    repositories: RepositoryBundle
    asset_store: AssetStore
    task_dispatcher: TaskDispatcher
    embedding_provider: EmbeddingProvider


def _build_repositories(settings: AppSettings) -> RepositoryContainer:
    if settings.profile == Profile.LOCAL_DEV:
        return RepositoryContainer(
            content=InMemoryContentRepository(),
            scans=InMemoryScanRepository(),
            disputes=InMemoryDisputeRepository(),
            alerts=InMemoryAlertRepository(),
            jobs=InMemoryJobRepository(),
            integrations=InMemoryIntegrationRepository(),
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


@lru_cache()
def get_container() -> AppContainer:
    settings = get_settings()
    configure_logging(settings)

    repositories = _build_repositories(settings)
    asset_store = _build_asset_store(settings)
    dispatcher = _build_task_dispatcher(settings)
    embedding_provider = _build_embedding_provider(settings)

    return AppContainer(
        settings=settings,
        repositories=repositories,
        asset_store=asset_store,
        task_dispatcher=dispatcher,
        embedding_provider=embedding_provider,
    )
