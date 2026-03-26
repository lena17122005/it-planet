from fastapi import APIRouter

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/pending-verification")
def pending_verification() -> dict:
    return {"items": []}
