from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SAEnum, DateTime, JSON, Text, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UrgencyLevel(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class FIRRecord(Base):
    __tablename__ = "fir_records"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=True)
    owner_description = Column(Text, nullable=False)
    visual_summary = Column(Text, nullable=True)
    affected_systems = Column(JSON, nullable=True)
    allergy_warnings = Column(JSON, nullable=True)
    immediate_care = Column(Text, nullable=True)
    urgency = Column(SAEnum(UrgencyLevel), default=UrgencyLevel.MODERATE)
    risk_score = Column(Float, nullable=True)
    full_report = Column(JSON, nullable=True)
    disclaimer = Column(Text, default="This is an AI-generated advisory report. Please consult a licensed veterinarian for diagnosis and treatment.")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dog = relationship("Dog", back_populates="fir_records")
