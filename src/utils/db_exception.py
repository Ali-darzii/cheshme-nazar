from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class ServerError(HTTPException):
    def __init__(self) -> None:
        status_code = 500
        detail = "Server Error"
        headers = None
        super().__init__(status_code, detail, headers)

class UniquenessException(HTTPException):
    def __init__(self):
        status_code = status.HTTP_409_CONFLICT
        headers=None
        detail = "Uniqueness issue accourd."
        super().__init__(status_code, detail, headers)
        
class ForeignKeyException(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        headers=None
        detail = "Related foreign key doesn't exist."
        super().__init__(status_code, detail, headers)
        
        
        
class PostgresException(Exception):
    db_errors = {
        "23505": UniquenessException,
        "23503": ForeignKeyException,
    }
    
    def __init__(self, error: IntegrityError):
        pgcode = getattr(error.orig, "pgcode", None)
        
        exc_class = self.db_errors.get(pgcode)
        if exc_class:
            raise exc_class()

        raise ServerError()