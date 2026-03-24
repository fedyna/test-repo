from __future__ import annotations
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import httpx
from app.core.config import settings


class IngestionService:
    """
    Hybrid mode (Option B):
      - Discovery/new uploads via public RSS feeds (no key)
      - Reliable metrics via YouTube Data API videos.list/channels.list (key, minimal quota)
    """

    async def fetch_channel_feed(self, channel_id: str) -> list[dict]:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url)
            r.raise_for_status()
        root = ET.fromstring(r.text)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        out = []
        for entry in root.findall("atom:entry", ns):
            video_id = entry.findtext("yt:videoId", default="", namespaces=ns)
            title = entry.findtext("atom:title", default="", namespaces=ns)
            published = entry.findtext("atom:published", default="", namespaces=ns)
            out.append(
                {
                    "yt_video_id": video_id,
                    "title": title,
                    "published_at": datetime.fromisoformat(published.replace("Z", "+00:00")) if published else datetime.now(timezone.utc),
                }
            )
        return out

    async def fetch_video_metrics(self, video_ids: list[str]) -> dict[str, dict]:
        if not video_ids:
            return {}
        if not settings.youtube_api_key:
            return {v: {"viewCount": 0, "likeCount": 0, "commentCount": 0} for v in video_ids}
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "statistics,contentDetails,snippet",
            "id": ",".join(video_ids[:50]),
            "key": settings.youtube_api_key,
            "maxResults": 50,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            payload = r.json()
        result = {}
        for item in payload.get("items", []):
            result[item["id"]] = {
                "viewCount": int(item.get("statistics", {}).get("viewCount", 0)),
                "likeCount": int(item.get("statistics", {}).get("likeCount", 0)),
                "commentCount": int(item.get("statistics", {}).get("commentCount", 0)),
                "duration": item.get("contentDetails", {}).get("duration", "PT0S"),
                "title": item.get("snippet", {}).get("title", ""),
                "description": item.get("snippet", {}).get("description", ""),
                "publishedAt": item.get("snippet", {}).get("publishedAt"),
                "tags": item.get("snippet", {}).get("tags", []),
                "channelId": item.get("snippet", {}).get("channelId", ""),
            }
        return result
