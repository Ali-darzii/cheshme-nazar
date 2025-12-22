from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.helper.exception import AuthErrorResponse
from src.auth.schema import TokenType
from src.config import oauth2_scheme
from src.core.postgres import get_postdb
from src.user.model import User as UserModel
from src.user.crud import user_crud
from src.utils.general_exception import GeneralErrorReponses
from src.auth.helper.jwt import jwt


async def get_current_user(
    db: AsyncSession = Depends(get_postdb),
    access_token: str = Depends(oauth2_scheme)
) -> UserModel:
    payload = jwt.verify_token(access_token, TokenType.access_token)
    email = payload.get("sub")
    if not email:
        raise GeneralErrorReponses.CREDENTIALS_EXCEPTION
    
    user = await user_crud.get_by_email(db, email)
    if not user:
        raise GeneralErrorReponses.CREDENTIALS_EXCEPTION

    if not user.email:
        raise AuthErrorResponse.APPROVE_EMAIL    
    
    return user