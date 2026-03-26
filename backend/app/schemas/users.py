from pydantic import BaseModel, EmailStr

from app.models.user import ProfileVisibility, UserRole


class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    role: UserRole
    email_verified: bool


class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    university: str | None = None
    graduation_year: int | None = None
    about: str | None = None
    skills: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None


class PrivacyUpdate(BaseModel):
    profile_visibility: ProfileVisibility
    show_responses: bool
    allow_contact_requests: bool
