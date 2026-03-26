from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.moderation import ModerationAction, ModerationEntity, ModerationLog
from app.models.tag import Tag
from app.models.user import User, UserRole
from app.models.vacancy import ModerationStatus, Vacancy
from app.schemas.tags import TagCreate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(require_role(UserRole.curator))):
    return {
        "pending_vacancies": db.query(Vacancy).filter(Vacancy.moderation_status == ModerationStatus.pending).count(),
        "tags_count": db.query(Tag).count(),
    }


@router.post("/tags")
def create_tag(payload: TagCreate, db: Session = Depends(get_db), _: User = Depends(require_role(UserRole.curator))):
    exists = db.query(Tag).filter(Tag.name.ilike(payload.name)).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag exists")

    tag = Tag(name=payload.name.strip())
    db.add(tag)
    db.commit()
    return {"status": "created", "id": tag.id}


@router.patch("/vacancies/{vacancy_id}/publish")
def publish_vacancy(vacancy_id: int, db: Session = Depends(get_db), curator: User = Depends(require_role(UserRole.curator))):
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    vacancy.moderation_status = ModerationStatus.published
    db.add(
        ModerationLog(
            curator_id=curator.id,
            entity=ModerationEntity.vacancy,
            entity_id=vacancy.id,
            action=ModerationAction.approve,
            comment="Published by curator",
        )
    )
    db.commit()
    return {"status": "published"}


@router.patch("/users/{user_id}/block")
def block_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role(UserRole.curator))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_blocked = True
    db.commit()
    return {"status": "blocked"}
