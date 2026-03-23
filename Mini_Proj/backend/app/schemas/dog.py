from pydantic import BaseModel, Field
from datetime import datetime
from app.models.dog import BreedEnum


class AllergyOut(BaseModel):
    id: int
    allergen_name: str
    category: str
    severity: str
    notes: str | None = None

    model_config = {"from_attributes": True}


class DogCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: BreedEnum
    age_years: float = Field(..., gt=0, le=30)
    weight_kg: float = Field(..., gt=0, le=100)
    owner_name: str = Field(..., min_length=1, max_length=100)
    image_url: str | None = None


class DogUpdate(BaseModel):
    name: str | None = None
    breed: BreedEnum | None = None
    age_years: float | None = Field(None, gt=0, le=30)
    weight_kg: float | None = Field(None, gt=0, le=100)
    owner_name: str | None = None
    image_url: str | None = None


class DogOut(BaseModel):
    id: int
    name: str
    breed: BreedEnum
    age_years: float
    weight_kg: float
    owner_name: str
    image_url: str | None = None
    created_at: datetime | None = None
    allergies: list[AllergyOut] = []

    model_config = {"from_attributes": True}


class DogListOut(BaseModel):
    dogs: list[DogOut]
    total: int
