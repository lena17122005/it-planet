from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    display_name: str
    password: str
    role: UserRole
    company_name: str | None = None
    inn: str | None = None
    corporate_email: EmailStr | None = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
