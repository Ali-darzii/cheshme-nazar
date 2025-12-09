from typing import List, Type, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from pydantic import BaseModel

from src.utils.db_exception import PostgresException
from src.utils.singleton import SingletonMeta

class BaseCrud(SingletonMeta):
    """
    - For create and update needs fields for schema and model to be same.
    """

    def __init__(self, model: Type[SQLModel]):
        self.model = model

    async def list_all(self, db: AsyncSession) -> List[SQLModel]:
        """ with no relation load """
        result = await db.exec(select(self.model))
        return result.all()

    async def get_by_id(self, db: AsyncSession, pk: int) -> SQLModel | None:
        result = await db.exec(
            select(self.model).where(self.model.id == pk)
        )
        return result.one_or_none()

    async def create(self, db: AsyncSession, obj_in: BaseModel) -> SQLModel:
        db_obj = self.model(**obj_in.model_dump())

        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError as e:
            await db.rollback()
            raise PostgresException(e)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: SQLModel,
        obj_in: Union[BaseModel, dict],
        partial: bool = False
    ) -> SQLModel:

        update_data = obj_in.model_dump(exclude_unset=partial) \
            if isinstance(obj_in, BaseModel) else obj_in

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError as e:
            await db.rollback()
            raise PostgresException(e)

        return db_obj

    async def delete(self, db: AsyncSession, db_obj: SQLModel) -> None:
        try:
            await db.delete(db_obj)
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            raise PostgresException(e)
