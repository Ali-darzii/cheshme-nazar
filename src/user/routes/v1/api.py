from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.user.schema import UpdateUser, UserOut
from src.core.postgres import get_postdb
from src.user.crud import user_crud
from src.user.schema import CreateUser
from src.auth.helper.encryption import UserPassword
from src.utils.auth import get_current_user
from src.utils.general_exception import GeneralErrorReponses
from src.user.model import User as UserModel

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
    
    
@router.patch("/user", response_model=UserOut, status_code=status.HTTP_200_OK)
async def delete_user(
    update_user: UpdateUser,
    db: AsyncSession = Depends(get_postdb),
    user: UserModel = Depends(get_current_user)
) -> UserOut:
    if update_user.email and update_user.email != user.email:
        user.email_approved = False
        if await user_crud.get_by_email(db, update_user.email):
            raise GeneralErrorReponses.uniqueness("Email")
    
    return await user_crud.update(db, user, update_user, partial=True)


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_postdb),
    user: UserModel = Depends(get_current_user)
):
    await user_crud.soft_delete(db, user)