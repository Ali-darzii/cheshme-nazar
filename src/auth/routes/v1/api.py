from typing import Annotated

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.helper.jwt import Jwt, TokenType
from src.auth.schema import EmailApproveOtp, EmailSendOtp, TokenOut
from src.config import setting
from src.core.postgres import get_postdb
from src.core.redis import RedisService, get_redis
from src.user.crud import user_crud
from src.auth.helper.encryption import UserPassword
from src.utils.email import EmailSender, MessageProducer
from src.utils.general_exception import GeneralErrorReponses
from src.auth.helper.otp import generate_otp


router = APIRouter(
    prefix="/auth",
    tags=["v1 - auth"]
)


@router.post("/approve-email", status_code=status.HTTP_200_OK)
async def email_send_otp(
    approve_email: EmailSendOtp,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_postdb)
):
    user = user_crud.get_by_email(db, approve_email.email)
    if not user:
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    if user.email_approved:
        raise GeneralErrorReponses.bad_format("email_approved")
    
    redis_service = RedisService(redis)
    redis_key = f"email_{user.email}"
    
    if redis_service.get(redis_key):
        raise GeneralErrorReponses.TOO_MANY_REQUEST
    
    otp = generate_otp()    
    redis_service.set(redis_key, otp, setting.OTP_EXPIRE)
    
    msg = MessageProducer.send_otp(otp, setting.OTP_EXPIRE)
    # may need background task on this
    EmailSender.send([user.email], msg, "کد احراز هویت", subtype="html")
    
    
@router.put("/approve-email", status_code=status.HTTP_200_OK, response_model=TokenOut)
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
    
    otp = redis_service.get(redis_key)
    if not otp or int(otp) != approve_email.otp:
        raise GeneralErrorReponses.INVALID_TOKEN

    user = user_crud.email_approved(db, user)
    
    jwt = Jwt()
    access_token = jwt.create_token(user, TokenType.access_token)
    refresh_token = jwt.create_token(user, TokenType.refresh_token)
    
    return TokenOut(access_token=access_token, refresh_token=refresh_token, user_id=user.id)
    
    
    

@router.post("username/token", response_model=None, status_code=status.HTTP_201_CREATED)
async def username_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_postdb)
) -> None:
    form_data.username = form_data.username.lower()
    
    user = user_crud.get_by_username(db, form_data.username)
    if not user:
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    
    if not UserPassword.verify_password(form_data.password, user.password):
        raise GeneralErrorReponses.INVALID_CREDENTIALS
    
    jwt = Jwt()
    access_token = jwt.create_token(user, TokenType.access_token)
    refresh_token = jwt.create_token(user, TokenType.refresh_token)
    
    return None
    # return UserTokenOut(
    #     id=user.id,
    #     username=user.id,
    #     phone_number=user.phone_number,
    #     email=user.email,
    #     role=user.role,
    #     is_active=user.is_active,
    #     created_at=user.created_at,
    #     updated_at=user.updated_at,
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    