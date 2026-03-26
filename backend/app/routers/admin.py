from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def dashboard() -> dict:
    return {"message": "Curator moderation dashboard stub"}
