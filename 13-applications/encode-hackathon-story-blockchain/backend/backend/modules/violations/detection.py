from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable

from ..shared.models import (
    ContentAsset,
    RiskLevel,
    ScanMatchRecord,
    ScanRecord,
    ScanStatus,
    ViolationConfidence,
    ViolationRecord,
)
from ..shared.repositories import RepositoryBundle
from .evidence import EvidenceNotificationService
from .enforcement import StoryEnforcementService


@dataclass(slots=True)
class ViolationSettings:
    review_threshold: float = 0.7
    violation_threshold: float = 0.85


@dataclass
class ViolationDetectionService:
    repositories: RepositoryBundle
    evidence_service: EvidenceNotificationService
    enforcement_service: StoryEnforcementService
    settings: ViolationSettings = field(default_factory=ViolationSettings)

    async def evaluate_scan(self, scan: ScanRecord, matches: Iterable[ScanMatchRecord]) -> list[ViolationRecord]:
        violations: list[ViolationRecord] = []
        for match in matches:
            classification = self._classify(match.similarity_overall)
            if classification is None:
                continue
            asset = await self.repositories.content.get_asset(match.asset_id)
            if not asset:
                continue
            violation = await self._process_violation(
                asset=asset,
                scan=scan,
                match=match,
                confidence=match.similarity_overall,
                confidence_label=classification,
                infringing_url=scan.source_reference,
            )
            if violation:
                violations.append(violation)
        return violations

    async def evaluate_external_match(
        self,
        *,
        asset: ContentAsset,
        score: float,
        platform: str,
        infringing_url: str | None,
        semantic_snapshot: dict,
    ) -> ViolationRecord | None:
        classification = self._classify(score)
        if classification is None:
            return None

        synthetic_scan = ScanRecord(
            source_type=platform,
            source_reference=infringing_url or platform,
            status=ScanStatus.COMPLETED,
        )
        synthetic_match = ScanMatchRecord(
            scan_id=synthetic_scan.id,
            asset_id=asset.id,
            similarity_overall=score,
            similarity_breakdown={"fusion": score},
            risk_level=self._classify_risk(score),
        )
        return await self._process_violation(
            asset=asset,
            scan=synthetic_scan,
            match=synthetic_match,
            confidence=score,
            confidence_label=classification,
            infringing_url=infringing_url or platform,
            external_semantics=semantic_snapshot,
        )

    async def _process_violation(
        self,
        *,
        asset: ContentAsset,
        scan: ScanRecord,
        match: ScanMatchRecord,
        confidence: float,
        confidence_label: ViolationConfidence,
        infringing_url: str | None,
        external_semantics: dict | None = None,
    ) -> ViolationRecord | None:
        canonical = asset.semantic_fingerprint.get("canonical")
        canonical_hash = asset.semantic_fingerprint.get("canonical_hash")
        if not canonical or not canonical_hash:
            return None

        semantic_diff = self._build_semantic_diff(
            canonical=canonical,
            match=match,
            scan=scan,
            external_semantics=external_semantics,
        )

        evidence = await self.evidence_service.store_evidence(
            asset=asset,
            scan=scan,
            match=match,
            original_hash=canonical_hash,
            infringing_url=infringing_url,
            semantic_diff=semantic_diff,
            confidence=confidence,
        )

        violation = ViolationRecord(
            asset_id=asset.id,
            scan_id=scan.id,
            match_id=match.id,
            confidence=confidence_label,
            evidence_id=evidence.id,
            infringing_url=infringing_url,
            status="pending-review" if confidence_label == ViolationConfidence.REVIEW else "open-case",
        )
        violation = await self.repositories.violations.create_violation(violation)

        await self.evidence_service.dispatch_notifications(
            asset=asset,
            evidence=evidence,
            violation=violation,
        )

        await self.enforcement_service.report_violation(
            content_hash=canonical_hash,
            infringing_url=infringing_url,
            evidence_hash=evidence.evidence_hash,
        )

        return violation

    def _classify(self, score: float) -> ViolationConfidence | None:
        """
        Classify violation confidence based on similarity score.
        
        Higher scores map to higher confidence levels:
        - CRITICAL: score >= violation_threshold (0.85) - highest confidence, clear violation
        - LIKELY: score >= 0.75 and < violation_threshold - high confidence, likely violation
        - REVIEW: score >= review_threshold (0.7) and < 0.75 - moderate confidence, needs manual review
        - None: score < review_threshold (0.7) - below threshold, not processed as violation
        """
        if score >= self.settings.violation_threshold:
            return ViolationConfidence.CRITICAL
        if score >= 0.75:  # Intermediate threshold for LIKELY confidence
            return ViolationConfidence.LIKELY
        if score >= self.settings.review_threshold:
            return ViolationConfidence.REVIEW
        return None

    @staticmethod
    def _classify_risk(similarity: float) -> RiskLevel:
        """Classify risk level based on similarity score."""
        if similarity >= 0.7:
            return RiskLevel.HIGH
        if similarity >= 0.6:
            return RiskLevel.MODERATE
        return RiskLevel.LOW

    @staticmethod
    def _build_semantic_diff(
        *,
        canonical: dict,
        match: ScanMatchRecord,
        scan: ScanRecord,
        external_semantics: dict | None = None,
    ) -> dict:
        return {
            "canonical": canonical,
            "scan_fingerprint": scan.fingerprint.model_dump() if scan.fingerprint else {},
            "external_semantics": external_semantics or {},
            "similarity_overall": match.similarity_overall,
            "similarity_breakdown": match.similarity_breakdown,
            "recorded_at": datetime.utcnow().isoformat(),
        }
