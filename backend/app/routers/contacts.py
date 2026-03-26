from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.contact import ContactRequest, ContactRequestStatus
from app.models.user import User, UserRole
from app.schemas.contacts import ContactRequestCreate

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/request")
def send_request(payload: ContactRequestCreate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    if payload.receiver_id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot add yourself")

    receiver = db.query(User).filter(User.id == payload.receiver_id, User.role == UserRole.seeker).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seeker not found")
    if not receiver.allow_contact_requests:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User disabled contact requests")

    existing = db.query(ContactRequest).filter(
        or_(
            (ContactRequest.requester_id == user.id) & (ContactRequest.receiver_id == payload.receiver_id),
            (ContactRequest.requester_id == payload.receiver_id) & (ContactRequest.receiver_id == user.id),
        )
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request already exists")

    item = ContactRequest(requester_id=user.id, receiver_id=payload.receiver_id)
    db.add(item)
    db.commit()
    return {"status": "sent"}


@router.post("/request/{request_id}/accept")
def accept_request(request_id: int, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    item = db.query(ContactRequest).filter(ContactRequest.id == request_id, ContactRequest.receiver_id == user.id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    item.status = ContactRequestStatus.accepted
    db.commit()
    return {"status": "accepted"}


@router.get("")
def list_contacts(db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.seeker))):
    accepted = db.query(ContactRequest).filter(
        ContactRequest.status == ContactRequestStatus.accepted,
        or_(ContactRequest.requester_id == user.id, ContactRequest.receiver_id == user.id),
    ).all()
    return {"items": [{"id": c.id, "requester_id": c.requester_id, "receiver_id": c.receiver_id} for c in accepted]}
