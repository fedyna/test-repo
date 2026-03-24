from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import text
from app.core.config import settings
from app.db.session import SessionLocal

router = APIRouter()
security = HTTPBasic()


def require_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != settings.basic_auth_user or credentials.password != settings.basic_auth_password:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/health")
def health():
    return {"ok": True}


@router.get("/trending")
def trending(region: str = "MIX", _: None = Depends(require_auth)):
    session = SessionLocal()
    try:
        where = ""
        params = {}
        if region in {"RU", "US"}:
            where = "WHERE c.region = :region"
            params["region"] = region
        q = text(
            f"""
            SELECT v.yt_video_id, v.title, c.title as channel_title, c.region, s.score_total,
                   s.views_velocity, s.relative_views_z, s.acceleration, s.explanation_json
            FROM video_scores s
            JOIN videos v ON v.yt_video_id = s.yt_video_id
            JOIN channels c ON c.yt_channel_id = v.yt_channel_id
            {where}
            ORDER BY s.score_total DESC
            LIMIT 100
            """
        )
        rows = [dict(r._mapping) for r in session.execute(q, params).all()]
        return rows
    finally:
        session.close()
