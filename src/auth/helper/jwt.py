from typing import Any, Dict
import jwt
from datetime import datetime, timedelta, timezone
from enum import Enum

from src.user.model import User as UserModel
from src.config import setting
from src.utils.general_exception import GeneralErrorReponses

class TokenType(str, Enum):
    access_token = "access"
    refresh_token = "refresh"

class Jwt:
    
    def normilize_token(self, token: str) -> str:
        return token.replace("Bearer ", "")
    
    def create_token(
        self,
        user: UserModel,
        token_type: TokenType,
        expires_delta: timedelta = timedelta(days=setting.ACCESS_EXPIRE)
    ) -> str:
        to_encode = {
            "sub": user.username,
            "role": user.role,
            "token_type": token_type
        }
        
        expire = datetime.now(timezone.utc) + expires_delta
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.JWT_ALGORITHM)

        return encoded_jwt
        
    
    def verify_token(self, token: str, token_type: TokenType) -> Dict[str, Any]:
        token = self.normalize_token(token)
        try:
            if not token:
                raise
            
            payload: dict = jwt.decode(token, key=setting.SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
            if payload["token_type"] != token_type:
                raise 
            
            return payload   
        except Exception:
            raise GeneralErrorReponses.INVALID_TOKEN