import asyncio

from src.core import celery_app
from src.auth.helper.otp import generate_otp
from src.config import setting
from src.core.redis import RedisService, get_redis
from src.utils.email import EmailSender, MessageProducer

@celery_app.task(queue="send_email_otp_bt")
def send_email_otp_bt(email: str):
    asyncio.run(_send_email_otp(email))
    
    
async def _send_email_otp(email: str):
    redis_service = RedisService(get_redis)
    redis_key = f"email_{email}"
    otp = generate_otp()    
    
    await redis_service.set(redis_key, otp, setting.OTP_EXPIRE)

    msg = MessageProducer.send_otp(otp, setting.OTP_EXPIRE)
    EmailSender.send([email], msg, "کد احراز هویت چشمه نظر", subtype="html")