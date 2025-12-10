from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.helper.jwt import Jwt, TokenType
from src.auth.schema import UserTokenOut
from src.core.postgres_db import get_postdb
from src.user.crud import user_crud
from src.auth.helper.encryption import UserPassword
from src.utils.general_exception import GeneralErrorReponses

router = APIRouter(
    prefix="/auth",
    tags=["v1 - auth"]
)

@router.post("username/token", response_model=UserTokenOut, status_code=status.HTTP_201_CREATED)
async def username_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_postdb)
) -> UserTokenOut:
    form_data.username = form_data.username.lower()
    
    user = user_crud.get_by_username(db, form_data.username)
    if not user:
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    
    if not UserPassword.verify_password(form_data.password, user.password):
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    
    jwt = Jwt()
    access_token = jwt.create_token(user, TokenType.access_token)
    refresh_token = jwt.create_token(user, TokenType.refresh_token)
    
    return UserTokenOut(
        id=user.id,
        username=user.id,
        phone_number=user.phone_number,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        access_token=access_token,
        refresh_token=refresh_token
    )
    