from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.helper.jwt import Jwt, TokenType
from src.user.schema import UserTokenOut
from src.core.postgres_db import get_postdb
from src.user.crud import user_crud
from src.user.schema import CreateUser
from src.auth.helper.encryption import UserPassword
from src.utils.general_exception import GeneralErrorReponses

router = APIRouter(
    prefix="/user",
    tags=["v1 - user"]
)

@router.post("/user", response_model=UserTokenOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user: CreateUser,
    db: AsyncSession = Depends(get_postdb)
) -> UserTokenOut:
    user = await user_crud.get_by_username(db, create_user.username)
    if user:
        if user.phone_number == create_user.phone_number:
            error_field = "Phone number"
            
        elif user.username == create_user.username:
            error_field = "Username"
            
        raise GeneralErrorReponses.uniqueness(error_field)
        
    create_user.password = UserPassword.generate_password_hash(create_user.password)
    
    user = await user_crud.create(db, create_user)
    
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
    