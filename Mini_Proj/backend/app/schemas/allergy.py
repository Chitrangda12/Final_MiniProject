from pydantic import BaseModel, Field
from app.models.allergy import AllergyCategory, AllergySeverity


class AllergyCreate(BaseModel):
    allergen_name: str = Field(..., min_length=1, max_length=100)
    category: AllergyCategory
    severity: AllergySeverity = AllergySeverity.MODERATE
    notes: str | None = None


class AllergyUpdate(BaseModel):
    allergen_name: str | None = None
    category: AllergyCategory | None = None
    severity: AllergySeverity | None = None
    notes: str | None = None


class AllergyOut(BaseModel):
    id: int
    dog_id: int
    allergen_name: str
    category: AllergyCategory
    severity: AllergySeverity
    notes: str | None = None

    model_config = {"from_attributes": True}


class AllergyBulkCreate(BaseModel):
    allergies: list[AllergyCreate]
