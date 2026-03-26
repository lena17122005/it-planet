from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ModerationEntity(str, Enum):
    company = "company"
    vacancy = "vacancy"
    tag = "tag"
    user = "user"


class ModerationAction(str, Enum):
    approve = "approve"
    reject = "reject"
    edit = "edit"


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    curator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    entity: Mapped[ModerationEntity] = mapped_column(SqlEnum(ModerationEntity), index=True)
    entity_id: Mapped[int] = mapped_column(index=True)
    action: Mapped[ModerationAction] = mapped_column(SqlEnum(ModerationAction))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
