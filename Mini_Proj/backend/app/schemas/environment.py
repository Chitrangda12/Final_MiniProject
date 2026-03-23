from pydantic import BaseModel, Field


class EnvironmentRiskRequest(BaseModel):
    dog_id: int
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class EnvironmentRiskOut(BaseModel):
    dog_name: str
    location: dict
    risk_score: float
    risk_level: str
    environmental_data: dict
    allergy_alerts: list[str]
    activity_guidance: list[dict]
    disclaimer: str = "Environmental risk data is approximate. Monitor your pet and consult a vet for unusual symptoms."


class OutdoorScheduleRequest(BaseModel):
    location: str = Field(..., min_length=2, max_length=120)
    dog_id: int
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class OutdoorScheduleSlot(BaseModel):
    time_slot: str
    risk_level: str
    recommendation: str


class OutdoorScheduleOut(BaseModel):
    dog_id: int
    dog_name: str
    location: str
    generated_at: str
    schedule: list[OutdoorScheduleSlot]
