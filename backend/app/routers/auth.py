"""Базовые auth-роуты. Полная реализация добавляется на следующих этапах."""

from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth import RegisterRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair)
def register(payload: RegisterRequest) -> TokenPair:
    # TODO: сохранить пользователя в БД, добавить отправку email-кода и валидацию компании.
    if payload.role == "employer" and not (payload.company_name and payload.inn and payload.corporate_email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employer fields are required")

    # Заглушка, чтобы можно было интегрировать фронт параллельно.
    return TokenPair(
        access_token=create_access_token(payload.email),
        refresh_token=create_refresh_token(payload.email),
    )
