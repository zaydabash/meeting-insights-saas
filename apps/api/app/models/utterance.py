from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Utterance(Base):
    __tablename__ = "utterances"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, index=True)
    speaker_id = Column(Integer, ForeignKey("speakers.id"), nullable=False, index=True)
    start_ms = Column(Float, nullable=False)
    end_ms = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)

    meeting = relationship("Meeting", back_populates="utterances")
    speaker = relationship("Speaker", back_populates="utterances")

