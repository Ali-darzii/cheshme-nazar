from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.schema import UserTokenOut
from src.core.postgres_db import get_postdb
from src.user.crud import user_crud
from src.user.schema import CreateUser, UserOut

router = APIRouter(
    prefix="/auth",
    tags=["v1 - auth"]
)

@router.post("/token", response_model=UserTokenOut, status_code=status.HTTP_201_CREATED)
def create_user_token(
    create_user: CreateUser,
    db: AsyncSession = Depends(get_postdb)
):
    user = user_crud.get_by_username(db, create_user.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with username: {user.username} exist."
        )