from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["v1 - auth"]
)

@router.post()
def create_user(
    
):
    pass