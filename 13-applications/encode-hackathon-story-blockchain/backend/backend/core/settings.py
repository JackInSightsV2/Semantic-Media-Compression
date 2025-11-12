from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Profile(str, Enum):
    """
    Deployment profile that determines which adapters the application loads.
    """

    LOCAL_DEV = "local-dev"
    SQLITE = "sqlite"
    POSTGRES = "postgres"
    SUPABASE_PROD = "supabase-prod"


class StorageProfile(str, Enum):
    LOCAL = "local"
    SUPABASE = "supabase"
    S3 = "s3"


class TaskDispatcherProfile(str, Enum):
    SYNC = "sync"
    CELERY = "celery"
    ASYNCIO = "asyncio"


class EmbeddingProviderProfile(str, Enum):
    MOCK = "mock"
    LOCAL_MODEL = "local-model"
    REMOTE_API = "remote-api"


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env", env_file_encoding="utf-8")

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    json_logs: bool = Field(default=False)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", env_file_encoding="utf-8")

    url: str | None = Field(default=None, description="Database connection string")
    pool_size: int = Field(default=10)
    echo: bool = Field(default=False)


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STORAGE_", env_file=".env", env_file_encoding="utf-8")

    bucket: str | None = None
    base_path: str = Field(default="data")
    supabase_url: str | None = None
    supabase_key: str | None = None


class StoryProtocolSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STORY_", env_file=".env", env_file_encoding="utf-8")

    wallet_private_key: str | None = Field(
        default=None, description="Private key for Story Protocol wallet (without 0x prefix)"
    )
    rpc_provider_url: str = Field(
        default="https://aeneid.storyrpc.io", description="RPC provider URL for Story Protocol"
    )
    chain_id: int = Field(default=1315, description="Chain ID (1315 for Aeneid testnet, 1514 for mainnet)")
    use_mock: bool = Field(
        default=True, description="Use mock Story Protocol client instead of real SDK"
    )
    spg_nft_contract: str | None = Field(
        default=None,
        description="SPG NFT contract address for minting new NFTs (optional, uses default if not set)",
    )


class ExternalIntegrationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EXT_", env_file=".env", env_file_encoding="utf-8")

    pinata_jwt: str | None = None
    story_protocol_api_key: str | None = None
    hf_api_token: str | None = None
    youtube_api_key: str | None = None
    instagram_access_token: str | None = None
    tiktok_api_key: str | None = None


class TaskSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASK_", env_file=".env", env_file_encoding="utf-8")

    broker_url: str | None = None
    result_backend: str | None = None


class AppSettings(BaseSettings):
    """
    Central application settings object used for dependency injection.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__")

    profile: Profile = Field(default=Profile.LOCAL_DEV)
    storage_profile: StorageProfile = Field(default=StorageProfile.LOCAL)
    task_profile: TaskDispatcherProfile = Field(default=TaskDispatcherProfile.SYNC)
    embedding_profile: EmbeddingProviderProfile = Field(default=EmbeddingProviderProfile.MOCK)

    api_prefix: str = Field(default="/api")
    environment: Literal["local", "ci", "staging", "production"] = Field(default="local")

    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    external: ExternalIntegrationSettings = Field(default_factory=ExternalIntegrationSettings)
    tasks: TaskSettings = Field(default_factory=TaskSettings)
    story: StoryProtocolSettings = Field(default_factory=StoryProtocolSettings)


@lru_cache()
def get_settings() -> AppSettings:
    """
    Cached accessor for application settings, honouring environment overrides.
    """

    return AppSettings()
