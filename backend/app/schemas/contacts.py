from pydantic import BaseModel


class ContactRequestCreate(BaseModel):
    receiver_id: int
