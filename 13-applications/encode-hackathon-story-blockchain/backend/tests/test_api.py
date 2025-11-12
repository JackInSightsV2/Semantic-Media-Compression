from __future__ import annotations

import asyncio
from uuid import UUID

from backend.core.container import get_container
from backend.modules.monitoring import MonitoringService
from backend.modules.semantic import SemanticPipeline


def test_registration_scan_dispute_dashboard_flow(client) -> None:
    upload_response = client.post(
        "/api/registration/uploads",
        data={"title": "Test Story", "asset_type": "text", "text": "Once upon a time in a hackathon."},
    )
    assert upload_response.status_code == 202
    upload_data = upload_response.json()
    asset_id = UUID(upload_data["asset_id"])

    # Fingerprint is built during upload (synchronous dispatcher)
    registration_detail = client.get(f"/api/registration/{asset_id}")
    assert registration_detail.status_code == 200
    detail_data = registration_detail.json()
    assert detail_data["asset"]["title"] == "Test Story"
    assert detail_data["fingerprints"]

    manifest = detail_data["asset"]["manifest"]
    assert manifest["derivatives"], "Manifest should contain derivative records"

    semantic = detail_data["asset"]["semantic_fingerprint"]
    assert "ipfs_cid" in semantic
    assert "zk_proof" in semantic
    assert "raw_text" not in semantic
    assert "canonical" in semantic
    assert semantic["canonical"]["text_semantics"]["tone"] == "neutral"
    assert semantic["canonical"]["embedding"], "Canonical embedding should be present"

    container = get_container()
    ciphertext = container.ipfs_client.fetch_content(semantic["ipfs_cid"])
    assert b"hackathon" not in ciphertext

    story_response = client.post(
        "/api/registration/register-story",
        json={
            "asset_id": str(asset_id),
            "metadata": {"chain": "testnet"},
        },
    )
    assert story_response.status_code == 200
    story_payload = story_response.json()
    assert story_payload["status"] == "registered"
    assert story_payload["ipfs_cid"] == semantic["ipfs_cid"]

    scan_response = client.post(
        "/api/scans",
        data={
            "source_type": "upload",
            "source_reference": "scan-1",
            "text": "Once upon a time in a hackathon with creative stories.",
        },
    )
    assert scan_response.status_code == 202
    scan_id = UUID(scan_response.json()["scan_id"])

    scan_detail = client.get(f"/api/scans/{scan_id}")
    assert scan_detail.status_code == 200
    scan_data = scan_detail.json()
    assert scan_data["matches"], "Scan should produce at least one match"
    top_match = scan_data["matches"][0]
    assert top_match["asset_id"] == str(asset_id)

    options_response = client.get("/api/disputes/options")
    assert options_response.status_code == 200
    options = options_response.json()
    assert any(asset["id"] == str(asset_id) for asset in options["assets"])

    dispute_response = client.post(
        "/api/disputes",
        json={
            "asset_id": str(asset_id),
            "suspect_reference": str(scan_id),
            "notes": "Potential infringement detected.",
        },
    )
    assert dispute_response.status_code == 201
    dispute_id = UUID(dispute_response.json()["dispute"]["id"])

    dispute_detail = client.get(f"/api/disputes/{dispute_id}")
    assert dispute_detail.status_code == 200
    assert dispute_detail.json()["dispute"]["suspect_reference"] == str(scan_id)

    active_disputes = client.get("/api/disputes/active")
    assert active_disputes.status_code == 200
    assert any(dispute["id"] == str(dispute_id) for dispute in active_disputes.json())

    summary = client.get("/api/dashboard/summary")
    assert summary.status_code == 200
    summary_data = summary.json()
    assert summary_data["registered_assets"] >= 1
    assert summary_data["active_disputes"] >= 1

    activity = client.get("/api/dashboard/activity", params={"range": "7d"})
    assert activity.status_code == 200
    assert isinstance(activity.json(), list)

    notifications = client.get("/api/dashboard/notifications")
    assert notifications.status_code == 200
    notifications_data = notifications.json()
    assert notifications_data, "High-risk match should generate notification"

    insights = client.get("/api/dashboard/insights")
    assert insights.status_code == 200
    assert insights.json()

    # Plaintext opt-out path
    no_encrypt_response = client.post(
        "/api/registration/uploads",
        data={
            "title": "Plain Story",
            "asset_type": "text",
            "text": "Visible excerpt for public domain.",
            "encrypt": "false",
        },
    )
    assert no_encrypt_response.status_code == 202
    plain_asset_id = UUID(no_encrypt_response.json()["asset_id"])
    plain_detail = client.get(f"/api/registration/{plain_asset_id}")
    assert plain_detail.status_code == 200
    plain_semantic = plain_detail.json()["asset"]["semantic_fingerprint"]
    assert plain_semantic["encryption_mode"] == "plaintext"
    plain_content = container.ipfs_client.fetch_content(plain_semantic["ipfs_cid"])
    assert b"Visible excerpt" in plain_content
    assert "canonical_hash" in plain_semantic

    monitoring_service = MonitoringService(
        repositories=container.repositories,
        vector_index=container.vector_index,
        pipeline=SemanticPipeline(container.embedding_provider),
        platform_clients=container.platform_clients.values(),
        settings=container.monitoring_settings,
    )
    events = asyncio.run(monitoring_service.run_monitoring())
    assert events, "Monitoring service should surface at least one potential match"
