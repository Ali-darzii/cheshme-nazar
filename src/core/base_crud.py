from typing import List, Type

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.utils.postgres_exception import PostgresException
from src.utils.singleton import SingletonMeta
from src.core.base_model import Base as BaseModel
from pydantic import BaseModel as BaseSchema

class BaseCrud(SingletonMeta):
    """
    - For create and update needs to fields for schema and model be same.
    """
    
    def __init__(self, model: Type[BaseModel], db: Session):
        self.model = model
        self.db = db
        
    def list_all(self) -> List[Type[BaseModel]]:
        """ with no selectinload """
        return self.db.execute(select(self.model)).scalars().all()
    
    def get_by_id(self, pk: int) -> Type[BaseModel] | None:
        return self.db.execute(
            select(self.model).where(self.model.id == pk)
        ).scalar_one_or_none()
    
    def create(self, obj_in: Type[BaseSchema]) -> Type[BaseModel]:
        db_obj = self.model(**obj_in.model_dump())
        
        try:
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except IntegrityError as e:
            self.db.rollback()
            raise PostgresException(e)
        
        return db_obj
    
    def update(self, db_obj: Type[BaseModel], obj_in: Type[BaseSchema], partial=False) -> Type[BaseModel]:
        update_data = obj_in.model_dump(exclude_unset=partial)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        try:
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except IntegrityError as e:
            self.db.rollback()
            raise PostgresException(e)

        return db_obj
        