from sqlmodel import select, or_
from core.base_crud import BaseCrud

from sqlmodel.ext.asyncio.session import AsyncSession

from src.user.model import User as UserModel

class UserCrud(BaseCrud):
    async def get_by_username_or_phone_number(self, db: AsyncSession, username: str, phone_number: str) -> UserModel | None:
        result =  db.exec(
            select(self.model).where(
                or_(
                    self.model.username == username,
                    self.model.phone_number == phone_number
                )
            )
        )
        return result.one_or_none()
    
    
user_crud = UserCrud(UserModel)