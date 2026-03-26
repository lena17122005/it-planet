from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ResponseStatus(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    reserve = "reserve"
    pending = "pending"


class VacancyResponse(Base):
    __tablename__ = "vacancy_responses"
    __table_args__ = (UniqueConstraint("vacancy_id", "seeker_id", name="uq_vacancy_response"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), index=True)
    seeker_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[ResponseStatus] = mapped_column(SqlEnum(ResponseStatus), default=ResponseStatus.pending)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
