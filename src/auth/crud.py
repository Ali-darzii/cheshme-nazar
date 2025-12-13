from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.crud import BaseCrud
from src.auth.model import RevokedToken as RevokedTokenModel

class RevokedTokenCrud(BaseCrud):
    def __init__(self, model: RevokedTokenModel):
        self.model = model
        
    async def is_revoked_token(self, db: AsyncSession, jti: str) -> bool:
        result = await db.execute(
            select(self.model).where(self.model.jti == jti)
        )
        return bool(result.one_or_none())
    
    
revoked_token_crud = RevokedTokenCrud(RevokedTokenModel)