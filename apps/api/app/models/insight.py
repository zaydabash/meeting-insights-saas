from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Float, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class InsightType(str, enum.Enum):
    ACTION_ITEM = "action_item"
    DECISION = "decision"
    SENTIMENT = "sentiment"
    SUMMARY = "summary"
    NOTE = "note"


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, index=True)
    type = Column(SQLEnum(InsightType), nullable=False, index=True)
    text = Column(Text, nullable=False)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    confidence = Column(Float, nullable=True)
    extra = Column(JSON, nullable=True)  # Additional metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="insights")
    owner = relationship("User", back_populates="insights")

