from uuid import uuid4
from typing import Any, Dict
import jwt
from datetime import datetime, timedelta, timezone

from src.auth.schema import TokenType
from src.user.model import User as UserModel
from src.config import setting
from src.utils.general_exception import GeneralErrorReponses
from src.utils.singleton import SingletonMeta


class Jwt(metaclass=SingletonMeta):
    
    def normilize_token(self, token: str) -> str:
        return token.replace("Bearer ", "")
    
    def create_token(
        self,
        user: UserModel,
        token_type: TokenType,
        expires_delta: timedelta = timedelta(days=setting.ACCESS_EXPIRE)
    ) -> str:
        to_encode = {
            "sub": user.email,
            "role": user.role,
            "token_type": token_type,
            "jti": str(uuid4())
        }
        
        expire = datetime.now(timezone.utc) + expires_delta
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.JWT_ALGORITHM)

        return encoded_jwt
        
    def token_payload(self, token: str) -> Dict[str, Any]:
        token = self.normilize_token(token)
        try:
            return jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.JWT_ALGORITHM], options={"verify_exp": False})
        except Exception:
            raise GeneralErrorReponses.INVALID_TOKEN
    
    def verify_token(self, token: str, token_type: TokenType) -> Dict[str, Any]:
        """ token need to be healty and will return payload """
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
        
        
jwt = Jwt()