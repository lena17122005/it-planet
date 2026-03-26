from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(min_length=2, max_length=64)
