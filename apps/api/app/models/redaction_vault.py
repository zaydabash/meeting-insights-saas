from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RedactionVault(Base):
    __tablename__ = "redaction_vaults"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    token = Column(String, nullable=False, unique=True, index=True)  # Reversible token
    kind = Column(String, nullable=False)  # e.g., "email", "phone", "credit_card", "name"
    value_ciphertext = Column(Text, nullable=False)  # Encrypted original value
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization")

