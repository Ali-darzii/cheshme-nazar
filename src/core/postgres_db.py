from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import setting
from contextlib import contextmanager

engine = create_engine(setting.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Any, Any, None]:
    """Function to inject database as dependency via fastapi functionalities.

    Yields:
        Generator[Any, Any, None]: database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
# scripts 
@contextmanager
def get_db_cm() -> Generator[Any, Any, None]:
    """
    Function to access database for scripts or out of scope of API.
    
    Yields:
        Generator[Any, Any, None]: database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()