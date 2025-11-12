from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app import create_app
from backend.core.container import get_container


@pytest.fixture()
def client() -> TestClient:
    get_container.cache_clear()
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
