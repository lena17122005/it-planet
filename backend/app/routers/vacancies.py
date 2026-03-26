from fastapi import APIRouter, Query

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("")
def list_vacancies(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0)) -> dict:
    return {"items": [], "limit": limit, "offset": offset}
