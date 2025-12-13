from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect

class Base(DeclarativeBase):
    
    def model_dump(self,* , exclude_unset=False) -> dict:
        mapper = inspect(self).mapper
        data = {}

        for column in mapper.column_attrs:
            key = column.key
            value = getattr(self, key)
            if exclude_unset and value is None:
                continue

            data[key] = value

        return data