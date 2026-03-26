from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.company import Company
from app.models.response import VacancyResponse
from app.models.user import User, UserRole
from app.models.vacancy import Vacancy
from app.schemas.responses import ResponseCreate, ResponseStatusUpdate

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("")
def create_response(payload: ResponseCreate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    vacancy = db.query(Vacancy).filter(Vacancy.id == payload.vacancy_id, Vacancy.is_closed.is_(False)).first()
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    existing = db.query(VacancyResponse).filter(VacancyResponse.vacancy_id == payload.vacancy_id, VacancyResponse.seeker_id == user.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already responded")

    item = VacancyResponse(vacancy_id=payload.vacancy_id, seeker_id=user.id, note=payload.note)
    db.add(item)
    db.commit()
    return {"status": "created"}


@router.get("/mine")
def my_responses(db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    items = db.query(VacancyResponse).filter(VacancyResponse.seeker_id == user.id).all()
    return {"items": [{"id": r.id, "vacancy_id": r.vacancy_id, "status": r.status.value, "note": r.note} for r in items]}


@router.patch("/{response_id}")
def update_status(response_id: int, payload: ResponseStatusUpdate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.employer))):
    response = db.query(VacancyResponse).filter(VacancyResponse.id == response_id).first()
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Response not found")

    vacancy = db.query(Vacancy).filter(Vacancy.id == response.vacancy_id).first()
    company = db.query(Company).filter(Company.owner_id == user.id).first()
    if not vacancy or not company or vacancy.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    response.status = payload.status
    db.commit()
    return {"status": "updated"}
