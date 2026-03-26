from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.company import Company
from app.models.user import User, UserRole
from app.models.vacancy import ModerationStatus, Vacancy
from app.schemas.vacancies import VacancyCreate, VacancyOut
from app.services.geocoding import geocode_address

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

BANNED_WORDS = ["spam", "scam", "лохотрон"]


def _to_out(v: Vacancy) -> VacancyOut:
    return VacancyOut(
        id=v.id,
        company_id=v.company_id,
        title=v.title,
        description=v.description,
        type=v.type,
        format=v.format,
        city=v.city,
        salary_from=v.salary_from,
        salary_to=v.salary_to,
        latitude=v.latitude,
        longitude=v.longitude,
        tags=[t for t in v.tags_csv.split(",") if t],
        moderation_status=v.moderation_status.value,
    )


@router.get("")
def list_vacancies(
    db: Session = Depends(get_db),
    q: str | None = None,
    city: str | None = None,
    salary_from: int | None = None,
    salary_to: int | None = None,
    tags: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = db.query(Vacancy).filter(Vacancy.moderation_status == ModerationStatus.published, Vacancy.is_closed.is_(False))

    if q:
        query = query.filter(or_(Vacancy.title.ilike(f"%{q}%"), Vacancy.description.ilike(f"%{q}%")))
    if city:
        query = query.filter(Vacancy.city.ilike(f"%{city}%"))
    if salary_from is not None:
        query = query.filter(or_(Vacancy.salary_from.is_(None), Vacancy.salary_from >= salary_from))
    if salary_to is not None:
        query = query.filter(or_(Vacancy.salary_to.is_(None), Vacancy.salary_to <= salary_to))
    if tags:
        for tag in [t.strip() for t in tags.split(",") if t.strip()]:
            query = query.filter(Vacancy.tags_csv.ilike(f"%{tag}%"))

    items = query.offset(offset).limit(limit).all()
    return {"items": [_to_out(item) for item in items], "limit": limit, "offset": offset}


@router.post("", response_model=VacancyOut)
async def create_vacancy(payload: VacancyCreate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.employer))):
    company = db.query(Company).filter(Company.owner_id == user.id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company profile is required")

    text_for_moderation = f"{payload.title} {payload.description}".lower()
    moderation_status = ModerationStatus.published if not any(word in text_for_moderation for word in BANNED_WORDS) else ModerationStatus.pending

    vacancy = Vacancy(
        company_id=company.id,
        title=payload.title,
        description=payload.description,
        requirements=payload.requirements,
        city=payload.city,
        address=payload.address,
        salary_from=payload.salary_from,
        salary_to=payload.salary_to,
        type=payload.type,
        format=payload.format,
        expires_at=payload.expires_at,
        event_date=payload.event_date,
        tags_csv=",".join(payload.tags),
        moderation_status=moderation_status,
    )

    if payload.address:
        coords = await geocode_address(payload.address)
        if coords:
            vacancy.latitude = coords.lat
            vacancy.longitude = coords.lon

    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return _to_out(vacancy)


@router.post("/{vacancy_id}/close")
def close_vacancy(vacancy_id: int, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.employer))):
    company = db.query(Company).filter(Company.owner_id == user.id).first()
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy or not company or vacancy.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    vacancy.is_closed = True
    db.commit()
    return {"status": "closed"}
