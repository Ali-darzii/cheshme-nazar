from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.user.schema import UserOut
from src.core.postgres import get_postdb
from src.user.crud import user_crud
from src.user.schema import CreateUser
from src.auth.helper.encryption import UserPassword
from src.utils.general_exception import GeneralErrorReponses

router = APIRouter(
    prefix="/user",
    tags=["v1 - user"]
)

@router.post("/user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user: CreateUser,
    db: AsyncSession = Depends(get_postdb)
) -> UserOut:
    user = await user_crud.get_by_email(db, create_user.email)
    if user:
        raise GeneralErrorReponses.uniqueness("Email")
        
    create_user.password = UserPassword.generate_password_hash(create_user.password)
    
    user = await user_crud.create(db, create_user)
    
    return user
    