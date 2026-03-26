from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password, TokenError
from app.models.company import Company
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenPair, VerifyEmailRequest

router = APIRouter(prefix="/auth", tags=["auth"])

EMAIL_CODE = "123456"  # Demo code for MVP.


@router.post("/register", response_model=TokenPair)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenPair:
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=payload.email,
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()

    if payload.role == UserRole.employer:
        if not (payload.company_name and payload.inn and payload.corporate_email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employer fields are required")

        company = Company(
            owner_id=user.id,
            name=payload.company_name,
            inn=payload.inn,
            corporate_email=payload.corporate_email,
            domain=payload.corporate_email.split("@")[-1],
            verification_method="email",
        )
        db.add(company)

    db.commit()

    return TokenPair(access_token=create_access_token(user.email), refresh_token=create_refresh_token(user.email))


@router.post("/verify-email")
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)) -> dict:
    if payload.code != EMAIL_CODE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code")

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.email_verified = True
    db.commit()
    return {"status": "verified"}


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenPair(access_token=create_access_token(user.email), refresh_token=create_refresh_token(user.email))


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenPair:
    try:
        token_payload = decode_token(payload.refresh_token, "refresh")
    except TokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user = db.query(User).filter(User.email == token_payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return TokenPair(access_token=create_access_token(user.email), refresh_token=create_refresh_token(user.email))
