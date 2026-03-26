from datetime import date

from pydantic import BaseModel, Field

from app.models.vacancy import VacancyType, WorkFormat


class VacancyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    requirements: str | None = None
    type: VacancyType
    format: WorkFormat
    city: str
    address: str | None = None
    salary_from: int | None = None
    salary_to: int | None = None
    expires_at: date | None = None
    event_date: date | None = None
    tags: list[str] = Field(default_factory=list)


class VacancyOut(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    type: VacancyType
    format: WorkFormat
    city: str
    salary_from: int | None
    salary_to: int | None
    latitude: float | None
    longitude: float | None
    tags: list[str]
    moderation_status: str
