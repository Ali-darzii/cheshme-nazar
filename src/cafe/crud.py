from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cafe.model import Cafe as CafeModel
from src.core.crud import BaseCrud
from src.core.model import Provider


class CafeCrud(BaseCrud):
    def __init__(self, model: CafeModel):
        self.model = model

    async def list_cafes_pk_by_provider(self, db: AsyncSession, provider: Provider) -> List[str]:
        result = await db.execute(
            select(self.model.out_source_pk)
            .where(self.model.provider == provider)
        )
        return result.all()


cafe_crud = CafeCrud(CafeModel)