from celery import Celery
from app.config import settings

celery_app = Celery(
    "dostai",
    broker=settings.redis_url,
    backend=settings.redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Karachi",
    enable_utc=True,
)

# Import tasks
# from app.tasks import send_reminder_task
