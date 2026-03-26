from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserRole(str, Enum):
    seeker = "seeker"
    employer = "employer"
    curator = "curator"


class ProfileVisibility(str, Enum):
    all = "all"
    contacts = "contacts"
    nobody = "nobody"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), index=True)

    # moderation + security
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # seeker profile
    full_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    university: Mapped[str | None] = mapped_column(String(180), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    about: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # privacy
    profile_visibility: Mapped[ProfileVisibility] = mapped_column(SqlEnum(ProfileVisibility), default=ProfileVisibility.all)
    show_responses: Mapped[bool] = mapped_column(Boolean, default=True)
    allow_contact_requests: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    company = relationship("Company", back_populates="owner", uselist=False)
