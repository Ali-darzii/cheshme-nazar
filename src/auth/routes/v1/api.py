from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from fastapi import APIRouter, Body, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.helper.exception import AuthErrorResponse
from src.auth.helper.jwt import jwt, TokenType
from src.auth.schema import CreateRevokeToken, EmailApproveOtp, EmailLogin, GetEmail, TokenOut, TokenVerifyOut
from src.auth.task import send_email_otp_bt
from src.config import setting
from src.core.postgres import get_postdb
from src.core.redis import RedisService, get_redis
from src.user.crud import user_crud
from src.auth.helper.encryption import UserPassword
from src.user.model import User as UserModel
from src.utils.email import EmailSender, MessageProducer
from src.utils.general_exception import GeneralErrorReponses
from src.auth.helper.otp import generate_otp
from src.auth.crud import revoked_token_crud
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["v1 - auth"]
)


@router.post("/email/approve", status_code=status.HTTP_200_OK)
async def email_send_otp(
    approve_email: GetEmail,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_postdb)
):
    user = await user_crud.get_by_email(db, approve_email.email)
    if not user:
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    if user.email_approved:
        raise GeneralErrorReponses.bad_format("email_approved")
    
    redis_service = RedisService(redis)
    redis_key = f"email_{user.email}"
    
    if await redis_service.get(redis_key):
        raise GeneralErrorReponses.TOO_MANY_REQUEST
    
    send_email_otp_bt.delay(user.email)
    
    
@router.put("/email/approve", status_code=status.HTTP_200_OK, response_model=TokenOut)
async def email_approve_otp(
    approve_email: EmailApproveOtp,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_postdb)
) -> TokenOut:
    user = user_crud.get_by_email(db, approve_email.email)
    if not user:
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    if user.email_approved:
        raise GeneralErrorReponses.bad_format("email_approved")

    redis_service = RedisService(redis)
    redis_key = f"email_{user.email}"
    
    otp = await redis_service.get(redis_key)
    if not otp or int(otp) != approve_email.otp:
        raise GeneralErrorReponses.INVALID_TOKEN

    user = await user_crud.email_approved(db, user)
    
    access_token = jwt.create_token(user, TokenType.access_token)
    refresh_token = jwt.create_token(user, TokenType.refresh_token)
    
    return TokenOut(access_token=access_token, refresh_token=refresh_token, user_id=user.id)
    

@router.post("/email/token", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
async def email_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_postdb)
) -> TokenOut:    
    """ aware Test User is string@gmail.com string """
    user = await user_crud.get_by_email(db, form_data.username)
    if not user:
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    
    if not UserPassword.verify_password(form_data.password, user.password):
            raise GeneralErrorReponses.INVALID_CREDENTIALS    
    
    if not user.email_approved:
        raise AuthErrorResponse.APPROVE_EMAIL
    
    access_token = jwt.create_token(user, TokenType.access_token)
    refresh_token = jwt.create_token(user, TokenType.refresh_token)
    
    return TokenOut(access_token=access_token, refresh_token=refresh_token, user_id=user.id)
    
    
@router.post("/token/refresh", response_model=TokenOut, status_code=status.HTTP_200_OK)
async def refresh_token(
    db: AsyncSession = Depends(get_postdb),
    refresh_token: str = Body(..., embed=True)
) -> TokenOut:
    payload = jwt.token_payload(refresh_token)
    jti = payload.get("jti")
    if not jti:
        raise GeneralErrorReponses.bad_format("jti")
    
    if await revoked_token_crud.is_revoked_token(db, jti):
        raise GeneralErrorReponses.REVOKE_TOKEN
    
    payload = jwt.verify_token(refresh_token, TokenType.refresh_token)
    email = payload.get("sub")
    if not email:
        raise GeneralErrorReponses.INVALID_CREDENTIALS

    user = await user_crud.get_by_email(db, email)
    if not user:
        GeneralErrorReponses.INVALID_TOKEN
    
    await revoked_token_crud.create(db, CreateRevokeToken(jti=jti, user_id=user.id))
    
    access_token = jwt.create_token(user, TokenType.access_token)
    refresh_token = jwt.create_token(user, TokenType.refresh_token)
    
    return TokenOut(access_token=access_token, refresh_token=refresh_token, user_id=user.id)

    
@router.get("/token/verify", response_model=TokenVerifyOut, status_code=status.HTTP_200_OK)
async def verfiy_token(
    access_token: str = Body(..., embed=True)
):
    jwt.verify_token(access_token, TokenType.access_token)
    
    access_token = jwt.normilize_token(access_token)
    
    return TokenVerifyOut(access_token=access_token, token_type=TokenType.access_token)


@router.post("/token/revoke", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_token(
    db: AsyncSession = Depends(get_postdb),
    refresh_token: str = Body(..., embed=True),
    user: UserModel = Depends(get_current_user)
):
    payload = jwt.verify_token(refresh_token, TokenType.refresh_token)
    jti = payload.get("jti")
    if not jti:
        raise GeneralErrorReponses.REVOKE_TOKEN
    
    if await revoked_token_crud.is_revoked_token(db, jti):
        raise GeneralErrorReponses.REVOKE_TOKEN
    
    await revoked_token_crud.create(db, CreateRevokeToken(jti=jti, user_id=user.id))