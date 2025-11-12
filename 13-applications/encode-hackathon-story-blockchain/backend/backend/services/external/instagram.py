from __future__ import annotations

import httpx

from .base import ExternalContentItem, PlatformClient


class InstagramClient(PlatformClient):
    name = "instagram"

    def __init__(
        self,
        access_token: str | None,
        *,
        timeout: float = 10.0,
        api_version: str = "v20.0",
    ) -> None:
        self._access_token = access_token
        self._timeout = timeout
        self._api_version = api_version

    async def fetch_candidates(self, keywords: list[str]) -> list[ExternalContentItem]:
        if not self._access_token:
            return []
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            media_endpoint = f"https://graph.instagram.com/me/media"
            params = {
                "fields": "id,caption,media_url,media_type,timestamp",
                "access_token": self._access_token,
                "limit": 10,
            }
            response = await client.get(media_endpoint, params=params)
            response.raise_for_status()
            payload = response.json()
            items = payload.get("data", [])

            results: list[ExternalContentItem] = []
            for item in items:
                caption: str = item.get("caption") or ""
                if not caption.strip():
                    continue
                if keywords and not self._has_keyword_overlap(caption, keywords):
                    continue
                metadata = {
                    "media_url": item.get("media_url"),
                    "media_type": item.get("media_type"),
                    "timestamp": item.get("timestamp"),
                }
                comments = await self._fetch_comments(client, item["id"])
                text_blob = "\n".join(filter(None, [caption, *comments]))
                results.append(
                    ExternalContentItem(
                        platform=self.name,
                        identifier=item["id"],
                        url=item.get("media_url"),
                        text=text_blob,
                        metadata=metadata,
                    )
                )
            # Optional hashtag expansion
            if keywords:
                hashtag_posts = await self._fetch_hashtag_posts(client, keywords)
                results.extend(hashtag_posts)
            return results

    async def _fetch_comments(self, client: httpx.AsyncClient, media_id: str) -> list[str]:
        endpoint = f"https://graph.instagram.com/{media_id}/comments"
        params = {"access_token": self._access_token, "limit": 10}
        try:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            payload = response.json()
            return [entry.get("text", "") for entry in payload.get("data", []) if entry.get("text")]
        except httpx.HTTPStatusError:
            return []

    async def _fetch_hashtag_posts(
        self,
        client: httpx.AsyncClient,
        keywords: list[str],
    ) -> list[ExternalContentItem]:
        results: list[ExternalContentItem] = []
        for keyword in keywords:
            search_endpoint = f"https://graph.facebook.com/{self._api_version}/ig_hashtag_search"
            params = {"user_id": "me", "q": keyword, "access_token": self._access_token}
            try:
                search_response = await client.get(search_endpoint, params=params)
                search_response.raise_for_status()
            except httpx.HTTPStatusError:
                continue
            hashtag_data = search_response.json().get("data", [])
            if not hashtag_data:
                continue
            hashtag_id = hashtag_data[0]["id"]
            media_endpoint = (
                f"https://graph.facebook.com/{self._api_version}/{hashtag_id}/recent_media"
            )
            media_params = {
                "user_id": "me",
                "fields": "id,caption,media_type,media_url,timestamp",
                "access_token": self._access_token,
                "limit": 5,
            }
            try:
                media_response = await client.get(media_endpoint, params=media_params)
                media_response.raise_for_status()
                media_payload = media_response.json()
            except httpx.HTTPStatusError:
                continue
            for media in media_payload.get("data", []):
                caption: str = media.get("caption") or ""
                if not caption.strip():
                    continue
                if not self._has_keyword_overlap(caption, keywords):
                    continue
                comments = await self._fetch_comments(client, media["id"])
                text_blob = "\n".join(filter(None, [caption, *comments]))
                results.append(
                    ExternalContentItem(
                        platform=self.name,
                        identifier=media["id"],
                        url=media.get("media_url"),
                        text=text_blob,
                        metadata={
                            "media_type": media.get("media_type"),
                            "timestamp": media.get("timestamp"),
                            "source": "hashtag",
                        },
                    )
                )
        return results

    @staticmethod
    def _has_keyword_overlap(text: str, keywords: list[str]) -> bool:
        lowered = text.lower()
        return any(keyword.lower() in lowered for keyword in keywords)
