from celery import Celery
import os

from .config import settings

celery_app = Celery(
    "arena",
    broker=settings.redis_url
    backend=settings.redis_url)
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "events"}
}
