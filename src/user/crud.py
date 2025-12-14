from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.core.crud import BaseCrud
from src.user.model import User as UserModel
from src.user.model import Profile as ProfileModel
from src.user.schema import CreateUser, UpdateUser
from src.utils.db_exception import PostgresException

class UserCrud(BaseCrud):
    async def get_by_id_with_profile_relation(self, db: AsyncSession, id: int) -> UserModel:
        result = await db.execute(
            select(self.model).where(self.model.id == id)
            .options(selectinload(self.model.profile))
        )
        return result.one_or_none()
    
    async def get_by_email_with_profile_relation(self, db: AsyncSession, email: str) -> UserModel:
        result = await db.execute(
            select(self.model).where(self.model.email == email)
            .options(selectinload(self.model.profile))
        )
        return result.one_or_none()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> UserModel | None:
        result = await db.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()
    
    async def email_approved(self, db: AsyncSession, user: UserModel) -> UserModel:
        user.email_approved = True
        
        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
        except IntegrityError as e:
            await db.rollback()    
            raise PostgresException(e)
        
        return user
    
    async def create(self, db: AsyncSession, obj_in: CreateUser) -> UserModel:
        user = UserModel(
            email=obj_in.email,
            password=obj_in.password,
        )
        
        profile = ProfileModel(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            user=user
        )
        
        try:
            db.add(user)
            db.add(profile)
            await db.commit()
            await db.refresh(user)
            
        except IntegrityError as e:
            await db.rollback()    
            raise PostgresException(e)
        
        return user
    
    async def update(self, db: AsyncSession, db_obj: UserModel, obj_in: UpdateUser, partial = False):
        if obj_in.first_name:
            db_obj.profile.first_name = obj_in.first_name
        if obj_in.last_name:
            db_obj.profile.last_name = obj_in.last_name
        
        return super().update(db, db_obj, obj_in, partial)

    async def soft_delete(self, db: AsyncSession, db_obj: UserModel) -> None:
        db_obj.is_deleted = True
        
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError as e:
            await db.rollback()
            raise PostgresException(e)
    
    
user_crud = UserCrud(UserModel)