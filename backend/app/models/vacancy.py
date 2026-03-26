from datetime import date, datetime
from enum import Enum

from sqlalchemy import Boolean, Date, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VacancyType(str, Enum):
    vacancy = "vacancy"
    internship = "internship"
    mentorship = "mentorship"
    event = "event"


class WorkFormat(str, Enum):
    office = "office"
    hybrid = "hybrid"
    remote = "remote"


class ModerationStatus(str, Enum):
    pending = "pending"
    published = "published"
    rejected = "rejected"


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # PostGIS can store geometry; for simplicity keep scalar coordinates for API contracts.
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    salary_from: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[VacancyType] = mapped_column(SqlEnum(VacancyType), index=True)
    format: Mapped[WorkFormat] = mapped_column(SqlEnum(WorkFormat), index=True)
    event_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expires_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    tags_csv: Mapped[str] = mapped_column(Text, default="")
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    moderation_status: Mapped[ModerationStatus] = mapped_column(SqlEnum(ModerationStatus), default=ModerationStatus.pending, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
