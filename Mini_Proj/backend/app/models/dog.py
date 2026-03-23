from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SAEnum, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class BreedEnum(str, enum.Enum):
    LABRADOR = "Labrador Retriever"
    SHIH_TZU = "Shih-Tzu"
    GOLDEN = "Golden Retriever"
    BEAGLE = "Beagle"
    GERMAN_SHEPHERD = "German Shepherd"


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    breed = Column(SAEnum(BreedEnum), nullable=False)
    age_years = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    owner_name = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    allergies = relationship("Allergy", back_populates="dog", cascade="all, delete-orphan")
    vaccinations = relationship("VaccinationRecord", back_populates="dog", cascade="all, delete-orphan")
    fir_records = relationship("FIRRecord", back_populates="dog", cascade="all, delete-orphan")
