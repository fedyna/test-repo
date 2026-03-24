from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Channel(Base):
    __tablename__ = "channels"
    yt_channel_id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String, index=True)
    language_guess: Mapped[str | None] = mapped_column(String)
    subscribers: Mapped[int | None] = mapped_column(Integer)
    total_views: Mapped[int | None] = mapped_column(Integer)
    video_count: Mapped[int | None] = mapped_column(Integer)
    relevance_score: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String, default="active")
    discovered_by: Mapped[str] = mapped_column(String, default="search")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Video(Base):
    __tablename__ = "videos"
    yt_video_id: Mapped[str] = mapped_column(String, primary_key=True)
    yt_channel_id: Mapped[str] = mapped_column(ForeignKey("channels.yt_channel_id"), index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    duration_seconds: Mapped[int] = mapped_column(Integer)
    is_short: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[dict | None] = mapped_column(JSON)
    language_guess: Mapped[str | None] = mapped_column(String)
    cluster_id: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    yt_video_id: Mapped[str] = mapped_column(ForeignKey("videos.yt_video_id"), index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    view_count: Mapped[int] = mapped_column(Integer)
    like_count: Mapped[int] = mapped_column(Integer)
    comment_count: Mapped[int] = mapped_column(Integer)


class VideoScore(Base):
    __tablename__ = "video_scores"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    yt_video_id: Mapped[str] = mapped_column(ForeignKey("videos.yt_video_id"), index=True)
    window_hours: Mapped[int] = mapped_column(Integer)
    captured_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    score_total: Mapped[float] = mapped_column(Float)
    views_velocity: Mapped[float] = mapped_column(Float)
    likes_velocity: Mapped[float] = mapped_column(Float)
    comments_velocity: Mapped[float] = mapped_column(Float)
    acceleration: Mapped[float] = mapped_column(Float)
    relative_views_z: Mapped[float] = mapped_column(Float)
    relative_engagement_z: Mapped[float] = mapped_column(Float)
    cluster_id: Mapped[int | None] = mapped_column(Integer)
    explanation_json: Mapped[dict] = mapped_column(JSON)


class Cluster(Base):
    __tablename__ = "clusters"
    cluster_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    seed_keywords: Mapped[dict] = mapped_column(JSON)
    description: Mapped[str] = mapped_column(Text)


class Setting(Base):
    __tablename__ = "settings"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[dict] = mapped_column(JSON)
