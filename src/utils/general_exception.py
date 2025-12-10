from fastapi import HTTPException, status

class GeneralErrorReponses:
    _BAD_FORMAT = {"detail": "{} is in bad format.", "error_code": 0}
    _UNIQUENESS = {"detail": "{} need to be unique.", "error_code": 1}
    
    INVALID_TOKEN = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"detail": "Session has been expired.", "error_code": 2}
    )
    INVALID_CREDENTIALS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"detail": "Wrong Credential.", "error_code": 3}
    )
    REVOKE_TOKEN = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"detail": "Session has been expired", "error_code": 4}
    )
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"detail": "Credential error.", "error_code": 5}   
    )
    
    @classmethod
    def bad_format(cls, field: str) -> HTTPException:
        error = cls._BAD_FORMAT.copy()
        error["detail"] = error["detail"].format(field)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=cls.BAD_FORMAT
        ) 
        
    @classmethod
    def uniqueness(cls, field: str) -> HTTPException:
        error = cls._UNIQUENESS.copy()
        error["detail"] = error["detail"].format(field)
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=cls.BAD_FORMAT
        ) 
        
    @classmethod
    def invalid_token(cls) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=cls.INVALID_TOKEN
        )
        