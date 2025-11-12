from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrganizationResponse(BaseModel):
    id: int
    name: str
    domain: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

