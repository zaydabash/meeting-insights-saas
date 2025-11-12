from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.insight import InsightType


class InsightResponse(BaseModel):
    id: int
    meeting_id: int
    type: InsightType
    text: str
    owner_user_id: Optional[int] = None
    due_date: Optional[datetime] = None
    confidence: Optional[float] = None
    extra: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InsightCreate(BaseModel):
    meeting_id: Optional[int] = None
    text: Optional[str] = None
    type: InsightType
    text_content: str  # For extraction endpoint

