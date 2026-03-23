from pydantic import BaseModel, Field
from app.models.fir import UrgencyLevel


class FIRRequest(BaseModel):
    dog_id: int
    description: str = Field(..., min_length=10, max_length=2000)


class FIROut(BaseModel):
    id: int
    dog_id: int
    visual_summary: str | None = None
    affected_systems: list[str] = []
    allergy_warnings: list[str] = []
    immediate_care: str | None = None
    urgency: UrgencyLevel
    risk_score: float | None = None
    disclaimer: str
    full_report: dict | None = None

    model_config = {"from_attributes": True}
