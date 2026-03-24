from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery = Celery("trendradar", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.timezone = "UTC"
celery.conf.beat_schedule = {
    "ru-morning": {"task": "app.workers.jobs.run_region", "schedule": crontab(minute=0, hour=5), "args": ("RU",)},
    "ru-evening": {"task": "app.workers.jobs.run_region", "schedule": crontab(minute=0, hour=17), "args": ("RU",)},
    "us-morning": {"task": "app.workers.jobs.run_region", "schedule": crontab(minute=0, hour=16), "args": ("US",)},
    "us-evening": {"task": "app.workers.jobs.run_region", "schedule": crontab(minute=0, hour=4), "args": ("US",)},
}
celery.autodiscover_tasks(["app.workers.jobs"])
