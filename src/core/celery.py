from celery import Celery

from src.config import setting


app = Celery(
    "src",
    broker=setting.REDIS_BROKER_URL, # for now we using redis till need rabitmq
    backend=setting.REDIS_BROKER_URL,
)

app.autodiscover_tasks([
    "src.auth"
])
