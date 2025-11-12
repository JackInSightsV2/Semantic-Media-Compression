from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .base import ExternalContentItem, PlatformClient


class YouTubeClient(PlatformClient):
    name = "youtube"

    def __init__(self, api_key: str | None, *, timeout: float = 10.0) -> None:
        self._api_key = api_key
        self._timeout = timeout

    async def fetch_candidates(self, keywords: list[str]) -> list[ExternalContentItem]:
        if not self._api_key:
            return []
        query = " ".join(keywords) if keywords else ""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            search_params = {
                "part": "snippet",
                "type": "video",
                "maxResults": 5,
                "safeSearch": "none",
                "q": query,
                "key": self._api_key,
            }
            search_response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params=search_params,
            )
            search_response.raise_for_status()
            search_payload = search_response.json()
            video_ids = [item["id"]["videoId"] for item in search_payload.get("items", []) if "id" in item]
            if not video_ids:
                return []

            videos_task = asyncio.create_task(
                self._fetch_video_details(client, video_ids)
            )
            comments_task = asyncio.create_task(
                self._fetch_comments(client, video_ids)
            )
            captions_task = asyncio.create_task(
                self._fetch_captions(client, video_ids)
            )

            video_details, comments_map, captions_map = await asyncio.gather(
                videos_task, comments_task, captions_task, return_exceptions=False
            )

            results: list[ExternalContentItem] = []
            for video_id, detail in video_details.items():
                text_chunks = []
                snippet = detail.get("snippet", {})
                text_chunks.append(snippet.get("title") or "")
                text_chunks.append(snippet.get("description") or "")
                tags = snippet.get("tags") or []
                text_chunks.extend(tags)
                if captions := captions_map.get(video_id):
                    text_chunks.append(captions)
                if comments := comments_map.get(video_id):
                    text_chunks.extend(comments)

                combined = "\n".join(part for part in text_chunks if part)
                if not combined.strip():
                    continue

                results.append(
                    ExternalContentItem(
                        platform=self.name,
                        identifier=video_id,
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        text=combined,
                        metadata={
                            "publishedAt": snippet.get("publishedAt"),
                            "title": snippet.get("title"),
                            "tags": tags,
                        },
                    )
                )
            return results

    async def _fetch_video_details(
        self,
        client: httpx.AsyncClient,
        video_ids: list[str],
    ) -> dict[str, Any]:
        params = {
            "part": "snippet,contentDetails",
            "id": ",".join(video_ids),
            "key": self._api_key,
        }
        response = await client.get("https://www.googleapis.com/youtube/v3/videos", params=params)
        response.raise_for_status()
        payload = response.json()
        return {item["id"]: item for item in payload.get("items", [])}

    async def _fetch_comments(
        self,
        client: httpx.AsyncClient,
        video_ids: list[str],
    ) -> dict[str, list[str]]:
        comments: dict[str, list[str]] = {}
        for video_id in video_ids:
            params = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": 10,
                "textFormat": "plainText",
                "key": self._api_key,
            }
            try:
                response = await client.get(
                    "https://www.googleapis.com/youtube/v3/commentThreads",
                    params=params,
                )
                response.raise_for_status()
                payload = response.json()
                entries = []
                for item in payload.get("items", []):
                    top_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    entries.append(top_comment)
                if entries:
                    comments[video_id] = entries
            except httpx.HTTPStatusError:
                continue
        return comments

    async def _fetch_captions(
        self,
        client: httpx.AsyncClient,
        video_ids: list[str],
    ) -> dict[str, str]:
        # Captions require a second API call to list available caption tracks.
        captions: dict[str, str] = {}
        for video_id in video_ids:
            params = {
                "part": "snippet",
                "videoId": video_id,
                "key": self._api_key,
            }
            try:
                response = await client.get(
                    "https://www.googleapis.com/youtube/v3/captions",
                    params=params,
                )
                response.raise_for_status()
                payload = response.json()
                items = payload.get("items", [])
                if not items:
                    continue
                caption_id = items[0]["id"]
                download_params = {"key": self._api_key}
                download = await client.get(
                    f"https://www.googleapis.com/youtube/v3/captions/{caption_id}",
                    params=download_params,
                )
                if download.status_code == 200:
                    captions[video_id] = download.text
            except httpx.HTTPStatusError:
                continue
        return captions
