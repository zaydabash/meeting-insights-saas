from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class TaskStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskSource(str, enum.Enum):
    INTERNAL = "internal"
    SLACK = "slack"
    JIRA = "jira"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=True, index=True)
    title = Column(String, nullable=False)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.OPEN, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    source = Column(SQLEnum(TaskSource), nullable=False, default=TaskSource.INTERNAL)
    external_id = Column(String, nullable=True)  # e.g., Jira issue key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="tasks")
    meeting = relationship("Meeting", back_populates="tasks")
    owner = relationship("User", back_populates="tasks")

