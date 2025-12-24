from .celery import app as celery_app
from src.core.model import Comment

__all__ = (
    "celery_app",
    "Comment",
)