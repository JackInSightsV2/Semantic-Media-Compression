from __future__ import annotations

import httpx

from .base import ExternalContentItem, PlatformClient


class TikTokClient(PlatformClient):
    name = "tiktok"

    def __init__(
        self,
        api_key: str | None,
        *,
        timeout: float = 10.0,
        base_url: str = "https://open.tiktokapis.com/v2",
    ) -> None:
        self._api_key = api_key
        self._timeout = timeout
        self._base_url = base_url.rstrip("/")

    async def fetch_candidates(self, keywords: list[str]) -> list[ExternalContentItem]:
        if not self._api_key:
            return []
        headers = {"Authorization": f"Bearer {self._api_key}"}
        async with httpx.AsyncClient(timeout=self._timeout, headers=headers) as client:
            query = " ".join(keywords)
            video_endpoint = f"{self._base_url}/research/video/query/"
            params = {"keyword": query, "max_count": 5}
            try:
                response = await client.get(video_endpoint, params=params)
                response.raise_for_status()
                payload = response.json()
            except httpx.HTTPStatusError:
                return []

            data = payload.get("data", {})
            videos = data.get("videos", []) if isinstance(data, dict) else data
            results: list[ExternalContentItem] = []
            for video in videos:
                video_id = video.get("video_id")
                desc = video.get("desc") or ""
                if not video_id or not desc.strip():
                    continue
                comments = await self._fetch_comments(client, video_id)
                combined_text = "\n".join(filter(None, [desc, *comments]))
                results.append(
                    ExternalContentItem(
                        platform=self.name,
                        identifier=video_id,
                        url=video.get("share_url"),
                        text=combined_text,
                        metadata={
                            "create_time": video.get("create_time"),
                            "region": video.get("region"),
                        },
                    )
                )
            return results

    async def _fetch_comments(self, client: httpx.AsyncClient, video_id: str) -> list[str]:
        endpoint = f"{self._base_url}/research/comment/query/"
        params = {"video_id": video_id, "max_count": 10}
        try:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPStatusError:
            return []
        data = payload.get("data", {})
        comments = data.get("comments", []) if isinstance(data, dict) else data
        return [comment.get("text", "") for comment in comments if comment.get("text")]
