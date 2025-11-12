from __future__ import annotations

from dataclasses import dataclass

from ...services.story.protocol import StoryProtocolClient


@dataclass
class StoryEnforcementService:
    story_client: StoryProtocolClient

    async def report_violation(
        self,
        *,
        content_hash: str,
        infringing_url: str | None,
        evidence_hash: str,
    ) -> None:
        await self.story_client.report_violation(
            content_hash=content_hash,
            infringing_url=infringing_url,
            evidence_hash=evidence_hash,
        )
