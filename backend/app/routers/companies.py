from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.company import Company
from app.models.user import User, UserRole

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/me")
def my_company(db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.employer))):
    company = db.query(Company).filter(Company.owner_id == user.id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return {"id": company.id, "name": company.name, "is_verified": company.is_verified, "verification_method": company.verification_method}


@router.get("/pending-verification")
def pending_verification(
    db: Session = Depends(get_db),
    _curator: User = Depends(require_role(UserRole.curator)),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items = db.query(Company).filter(Company.is_verified.is_(False)).offset(offset).limit(limit).all()
    return {"items": [{"id": c.id, "name": c.name, "inn": c.inn, "corporate_email": c.corporate_email} for c in items], "limit": limit, "offset": offset}


@router.post("/{company_id}/verify")
def verify_company(company_id: int, db: Session = Depends(get_db), curator: User = Depends(require_role(UserRole.curator))):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    company.is_verified = True
    company.verification_method = "curator"
    company.verification_comment = f"Verified by curator {curator.id}"
    db.commit()
    return {"status": "verified"}
