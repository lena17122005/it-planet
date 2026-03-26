from pydantic import BaseModel

from app.models.response import ResponseStatus


class ResponseCreate(BaseModel):
    vacancy_id: int
    note: str | None = None


class ResponseStatusUpdate(BaseModel):
    status: ResponseStatus
