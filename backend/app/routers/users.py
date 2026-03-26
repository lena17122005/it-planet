from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.users import PrivacyUpdate, UserOut, UserProfileUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user, from_attributes=True)


@router.patch("/me/profile", response_model=UserOut)
def update_profile(payload: UserProfileUpdate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user, from_attributes=True)


@router.patch("/me/privacy")
def update_privacy(payload: PrivacyUpdate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    for field, value in payload.model_dump().items():
        setattr(user, field, value)
    db.commit()
    return {"status": "updated"}
