from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class MeetingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    calendar_event_id = Column(String, nullable=True, index=True)
    title = Column(String, nullable=False)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
    language = Column(String, nullable=True)
    duration_sec = Column(Float, nullable=True)
    audio_url = Column(String, nullable=True)
    transcript_text = Column(Text, nullable=True)
    status = Column(SQLEnum(MeetingStatus), nullable=False, default=MeetingStatus.PENDING, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization", back_populates="meetings")
    creator = relationship("User", back_populates="created_meetings")
    speakers = relationship("Speaker", back_populates="meeting", cascade="all, delete-orphan")
    utterances = relationship("Utterance", back_populates="meeting", cascade="all, delete-orphan")
    insights = relationship("Insight", back_populates="meeting", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="meeting")

