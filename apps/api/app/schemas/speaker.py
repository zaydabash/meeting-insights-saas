from pydantic import BaseModel
from typing import Optional


class SpeakerResponse(BaseModel):
    id: int
    meeting_id: int
    label: str
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True

