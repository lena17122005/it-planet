from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me() -> dict:
    return {"message": "Profile endpoint stub"}
