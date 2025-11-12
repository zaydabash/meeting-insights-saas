from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UsageMeter(Base):
    __tablename__ = "usage_meters"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    period_month = Column(String, nullable=False, index=True)  # Format: "2024-01"
    audio_minutes = Column(Float, nullable=False, default=0.0)
    tokens_in = Column(Integer, nullable=False, default=0)
    tokens_out = Column(Integer, nullable=False, default=0)
    storage_mb = Column(Float, nullable=False, default=0.0)
    cost_estimate = Column(Float, nullable=False, default=0.0)

    organization = relationship("Organization", back_populates="usage_meters")

