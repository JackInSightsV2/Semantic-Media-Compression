from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.container import AppContainer, get_container
from .modules.dashboard.api import router as dashboard_router
from .modules.dashboard.service import DashboardService
from .modules.disputes.api import router as disputes_router
from .modules.disputes.service import DisputeService
from .modules.monitoring import MonitoringService
from .modules.registration.api import router as registration_router
from .modules.registration.service import RegistrationService
from .modules.scans.api import router as scans_router
from .modules.scans.service import ScanService
from .modules.semantic import SemanticPipeline


def create_app() -> FastAPI:
    container = get_container()

    app = FastAPI(
        title="Encode Story Protection API",
        version="0.1.0",
        description="Backend services for the Encode Hackathon story protection MVP.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_routes(app, container)
    _register_events(app, container)

    @app.get("/healthz", tags=["health"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "profile": container.settings.profile.value}

    return app


def _register_routes(app: FastAPI, container: AppContainer) -> None:
    prefix = container.settings.api_prefix
    app.include_router(registration_router, prefix=prefix)
    app.include_router(scans_router, prefix=prefix)
    app.include_router(disputes_router, prefix=prefix)
    app.include_router(dashboard_router, prefix=prefix)


def _register_events(app: FastAPI, container: AppContainer) -> None:
    @app.on_event("startup")
    async def on_startup() -> None:
        shared_pipeline = SemanticPipeline(container.embedding_provider)

        registration_service = RegistrationService(
            repositories=container.repositories,
            asset_store=container.asset_store,
            task_dispatcher=container.task_dispatcher,
            embedding_provider=container.embedding_provider,
            vector_index=container.vector_index,
            encryption_service=container.encryption_service,
            ipfs_client=container.ipfs_client,
            story_client=container.story_client,
            semantic_pipeline=shared_pipeline,
        )
        scan_service = ScanService(
            repositories=container.repositories,
            task_dispatcher=container.task_dispatcher,
            embedding_provider=container.embedding_provider,
            vector_index=container.vector_index,
            semantic_pipeline=shared_pipeline,
        )
        dispute_service = DisputeService(
            repositories=container.repositories,
            asset_store=container.asset_store,
        )
        dashboard_service = DashboardService(repositories=container.repositories)
        monitoring_service = MonitoringService(
            repositories=container.repositories,
            vector_index=container.vector_index,
            pipeline=shared_pipeline,
            platform_clients=container.platform_clients.values(),
            settings=container.monitoring_settings,
        )

        await registration_service.register_tasks()
        await scan_service.register_tasks()

        app.state.registration_service = registration_service
        app.state.scan_service = scan_service
        app.state.dispute_service = dispute_service
        app.state.dashboard_service = dashboard_service
        app.state.monitoring_service = monitoring_service
