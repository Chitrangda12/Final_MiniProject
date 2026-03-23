from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum, DateTime, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class VaccineStatus(str, enum.Enum):
    SAFE = "safe"
    CONDITIONAL = "conditional"
    UNSAFE = "unsafe"


class VaccinationRecord(Base):
    __tablename__ = "vaccination_records"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
    vaccine_name = Column(String(100), nullable=False)
    status = Column(SAEnum(VaccineStatus), nullable=False)
    contraindications = Column(JSON, nullable=True)
    notes = Column(String(500), nullable=True)
    evaluated_at = Column(DateTime(timezone=True), server_default=func.now())

    dog = relationship("Dog", back_populates="vaccinations")
