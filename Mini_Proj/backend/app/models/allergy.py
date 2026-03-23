from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class AllergyCategory(str, enum.Enum):
    FOOD = "food"
    ENVIRONMENTAL = "environmental"
    MEDICATION = "medication"
    CONTACT = "contact"


class AllergySeverity(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
    allergen_name = Column(String(100), nullable=False)
    category = Column(SAEnum(AllergyCategory), nullable=False)
    severity = Column(SAEnum(AllergySeverity), default=AllergySeverity.MODERATE)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dog = relationship("Dog", back_populates="allergies")
