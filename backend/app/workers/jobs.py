from datetime import datetime, timezone, timedelta
from app.workers.celery_app import celery
from app.db.session import SessionLocal
from app.models.models import Video, VideoSnapshot, VideoScore
from app.services.ingestion import IngestionService
from app.services.filters import is_short_video
from app.services.scoring import compute_score, explanation_payload
from app.services.utils import parse_iso8601_duration_to_seconds


@celery.task(name="app.workers.jobs.run_region")
def run_region(region: str):
    # Simplified idempotent batch run
    session = SessionLocal()
    try:
        channel_ids = [row[0] for row in session.execute(
            "SELECT yt_channel_id FROM channels WHERE region=:r AND status IN ('active','pinned')",
            {"r": region},
        ).all()]
        ingestion = IngestionService()
        for channel_id in channel_ids:
            feed_items = __import__('asyncio').run(ingestion.fetch_channel_feed(channel_id))[:50]
            ids = [x["yt_video_id"] for x in feed_items if x.get("yt_video_id")]
            metrics = __import__('asyncio').run(ingestion.fetch_video_metrics(ids))
            for vid in ids:
                item = metrics.get(vid, {})
                duration = parse_iso8601_duration_to_seconds(item.get("duration", "PT0S"))
                title = item.get("title", "")
                tags = item.get("tags", [])
                if is_short_video(title, tags, duration):
                    continue
                published = item.get("publishedAt")
                if published:
                    pdt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    if pdt < datetime.now(timezone.utc) - timedelta(days=20):
                        continue
                v = session.get(Video, vid)
                if not v:
                    v = Video(
                        yt_video_id=vid,
                        yt_channel_id=item.get("channelId", channel_id),
                        title=title,
                        description=item.get("description", ""),
                        published_at=pdt,
                        duration_seconds=duration,
                        is_short=False,
                        tags=tags,
                        language_guess="ru" if region == "RU" else "en",
                    )
                    session.add(v)
                snap = VideoSnapshot(
                    yt_video_id=vid,
                    captured_at=datetime.now(timezone.utc),
                    view_count=item.get("viewCount", 0),
                    like_count=item.get("likeCount", 0),
                    comment_count=item.get("commentCount", 0),
                )
                session.add(snap)
                score_total, rel_v, rel_e = compute_score(
                    views_velocity=float(item.get("viewCount", 0))/24.0,
                    engagement_velocity=float(item.get("likeCount", 0)+item.get("commentCount", 0))/24.0,
                    acceleration=0.1,
                    freshness_bonus=1.0,
                    views_history=[1,2,3,4,5],
                    engagement_history=[1,1,2,2,3],
                    weights={"w1":0.45,"w2":0.3,"w3":0.15,"w4":0.1},
                )
                session.add(VideoScore(
                    yt_video_id=vid,
                    window_hours=24,
                    captured_at=datetime.now(timezone.utc),
                    score_total=score_total,
                    views_velocity=float(item.get("viewCount", 0))/24.0,
                    likes_velocity=float(item.get("likeCount", 0))/24.0,
                    comments_velocity=float(item.get("commentCount", 0))/24.0,
                    acceleration=0.1,
                    relative_views_z=rel_v,
                    relative_engagement_z=rel_e,
                    cluster_id=2,
                    explanation_json=explanation_payload(item.get("viewCount", 0), float(item.get("viewCount", 0))/24.0, rel_v, 0.1, "agents/code"),
                ))
        session.commit()
    finally:
        session.close()
