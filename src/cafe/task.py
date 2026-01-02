from src.core import celery_app
from src.out_source_auth.snap import SnapAnonymousAuth

@celery_app.task(queue="cafe_snap")
def scrape_snap_cafe():
    snap_auth = SnapAnonymousAuth()
    access_token = snap_auth.get_access_token()