from fastapi import APIRouter

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("")
def list_contacts() -> dict:
    return {"items": []}
