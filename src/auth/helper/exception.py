from fastapi import HTTPException, status

class AuthErrorResponse:
    APPROVE_EMAIL = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail={"detail":"Email need to be approved", "error_code": 1001}
    )