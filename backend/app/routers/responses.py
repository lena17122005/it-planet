from fastapi import APIRouter

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("")
def list_responses() -> dict:
    return {"items": []}
