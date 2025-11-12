from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.meeting import MeetingStatus
from app.schemas.speaker import SpeakerResponse
from app.schemas.insight import InsightResponse
from app.schemas.task import TaskResponse


class MeetingCreate(BaseModel):
    title: str
    occurred_at: datetime
    language: Optional[str] = None
    transcript_text: Optional[str] = None


class MeetingResponse(BaseModel):
    id: int
    org_id: int
    calendar_event_id: Optional[str] = None
    title: str
    occurred_at: datetime
    language: Optional[str] = None
    duration_sec: Optional[float] = None
    audio_url: Optional[str] = None
    transcript_text: Optional[str] = None
    status: MeetingStatus
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class MeetingDetailResponse(MeetingResponse):
    speakers: List[SpeakerResponse] = []
    insights: List[InsightResponse] = []
    tasks: List[TaskResponse] = []


class MeetingListResponse(BaseModel):
    items: List[MeetingResponse]
    total: int
    page: int
    page_size: int

