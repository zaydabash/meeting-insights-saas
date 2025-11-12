from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus, TaskSource


class TaskResponse(BaseModel):
    id: int
    org_id: int
    meeting_id: Optional[int] = None
    title: str
    owner_user_id: int
    status: TaskStatus
    due_date: Optional[datetime] = None
    source: TaskSource
    external_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    meeting_id: Optional[int] = None
    title: str
    owner_user_id: int
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    title: Optional[str] = None
    due_date: Optional[datetime] = None

