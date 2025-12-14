from fastapi.security import OAuth2PasswordBearer
from src.config._config import get_setting

setting = get_setting()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/API/v1/auth/token")



__all__ = (
    "setting",
    "oauth2_scheme",
)
