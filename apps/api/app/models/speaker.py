from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, index=True)
    label = Column(String, nullable=False)  # e.g., "SPEAKER_00", "SPEAKER_01"
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)

    meeting = relationship("Meeting", back_populates="speakers")
    utterances = relationship("Utterance", back_populates="speaker")

