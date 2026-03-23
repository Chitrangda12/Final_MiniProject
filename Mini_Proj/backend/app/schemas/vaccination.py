from pydantic import BaseModel
from app.models.vaccination import VaccineStatus


class VaccineEvaluation(BaseModel):
    vaccine_name: str
    status: VaccineStatus
    contraindications: list[str] = []
    reason: str


class VaccinationReportOut(BaseModel):
    dog_id: int
    dog_name: str
    breed: str
    allergies: list[str]
    evaluations: list[VaccineEvaluation]
    disclaimer: str = "This vaccination report is AI-generated guidance. Consult your veterinarian before making vaccination decisions."
