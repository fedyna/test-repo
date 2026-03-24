# YouTube Trend Radar (Self-hosted)

Production-oriented monorepo for RU/US YouTube automation+AI trend monitoring.

## Milestones
1. **Research + ingestion decision**: evaluate API-keyless OSS options and select compliant architecture.
2. **Core backend**: FastAPI API, Postgres schema, Celery scheduler/worker, Redis queue.
3. **Ingestion + scoring**: RSS discovery, minimal metrics retrieval, long-form filter, freshness windows, scoring + explainability.
4. **UI**: Next.js dashboard pages (Dashboard, Trending, Channels, Video Detail, Settings).
5. **Ops**: docker-compose, migrations/seeds, health checks, tests, deploy guide.

## Ingestion architecture choice
**Selected: Option B (Hybrid, compliant + reliable).**

- **Discovery/listing**: YouTube public RSS feeds (`/feeds/videos.xml?channel_id=...`) without API keys.
- **Reliable metrics (views/likes/comments + duration)**: minimal YouTube Data API v3 calls (`videos.list`, optionally `channels.list`) with quota-aware batching.

Why not pure keyless for metrics? Public compliant endpoints do not reliably expose full up-to-date stats per video/channel in a structured, stable way for production trend scoring.

## Candidate tool evaluation (GitHub research)
| Candidate | Data coverage | Maintenance | Compliance risk | Reliability risk | Integration effort |
|---|---|---|---|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | video metadata, subtitles, sometimes counts | active | Medium (extractor-based) | Medium | Medium |
| [Invidious](https://github.com/iv-org/invidious) | video/channel metadata via alt frontend API | Medium-active | Medium/High (depends on instance/proxy behavior) | Medium/High | High |
| [NewPipeExtractor](https://github.com/TeamNewPipe/NewPipeExtractor) | streams/metadata extraction | active | Medium | Medium/High | High |
| [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) | transcripts only | active | Low/Medium | Medium | Low |
| [YouTube RSS consumers](https://github.com/topics/youtube-rss) | upload discovery feed | varied | Low | Low | Low |

## Stack
- Backend: FastAPI + SQLAlchemy
- Worker/Scheduler: Celery + Beat
- DB: Postgres
- Queue: Redis
- Frontend: Next.js

## Run locally
```bash
docker compose up --build
```

API: `http://localhost:8000/api/health`  
Web: `http://localhost:3000`

## Migrations + seed
Inside backend container:
```bash
alembic upgrade head
psql postgresql://trendradar:trendradar@postgres:5432/trendradar -f seed.sql
```

## ENV vars
| Variable | Default | Description |
|---|---|---|
| DATABASE_URL | `postgresql+psycopg://trendradar:trendradar@postgres:5432/trendradar` | DB connection |
| REDIS_URL | `redis://redis:6379/0` | broker/backend |
| BASIC_AUTH_USER | `admin` | single-user auth login |
| BASIC_AUTH_PASSWORD | `admin` | single-user auth password |
| YOUTUBE_API_KEY | empty | required for reliable metrics in Option B |
| TELEGRAM_BOT_TOKEN | empty | digest bot token |
| TELEGRAM_CHAT_ID | empty | digest chat id |
| APP_ENV | `dev` | env mode |
| NEXT_PUBLIC_API_BASE | `http://localhost:8000` | web→api base |

## Scheduling defaults
- RU: `08:00`, `20:00` Europe/Moscow
- US: `08:00`, `20:00` America/Los_Angeles

Implemented in Celery beat as UTC cron equivalents.

## Scoring (configurable)
```
score_total = w1 * relative_views_z
            + w2 * relative_engagement_z
            + w3 * clamp(acceleration,-2,5)
            + w4 * freshness_bonus
```

Explainability JSON example:
```json
{
  "why": "24h views growth: +2400 (100.0/h); velocity +2.10σ vs channel baseline; acceleration +0.60",
  "cluster": "agents/code"
}
```

## Telegram digest
Worker can be extended to send RU/US/MIX top lists each scheduled run using `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`.

## VPS deployment (Ubuntu)
```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
# re-login
cd /opt && git clone <your-repo-url> trend-radar && cd trend-radar
docker compose up -d --build
```

## Tests
```bash
cd backend
pytest -q
```

## Notes
- Long-form filter excludes videos `< 90s` and titles/tags containing `shorts`.
- Freshness window default is 20 days.
- Hysteresis utility for promote/demote is included and covered by tests.
