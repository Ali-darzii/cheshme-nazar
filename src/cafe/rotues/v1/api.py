from fastapi import APIRouter, Depends, status

from src.cafe.task import scrape_snap_cafe
from src.user.model import User as UserModel
from src.utils.auth import get_current_user


router = APIRouter(
    prefix="/cafe",
    tags=["v1 - cafe"]
)


@router.post("/scrape-task", status_code=status.HTTP_200_OK)
def run_scrapte_task(
    user: UserModel = Depends(get_current_user),
):
    scrape_snap_cafe.delay()
    