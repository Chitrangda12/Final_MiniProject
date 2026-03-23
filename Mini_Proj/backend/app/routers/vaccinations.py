from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.dog import Dog
from app.services.vaccination_engine import VaccinationEngine
from app.schemas.vaccination import VaccinationReportOut

router = APIRouter(prefix="/api/v1/vaccinations", tags=["Vaccinations"])


@router.get("/{dog_id}/report", response_model=VaccinationReportOut)
async def get_vaccination_report(dog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dog).where(Dog.id == dog_id))
    dog = result.scalar_one_or_none()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    engine = VaccinationEngine(db)
    evaluations = await engine.evaluate_all_vaccines(dog_id)

    from app.services.allergy_filter import AllergyFilter
    af = AllergyFilter(db)
    allergies = await af.get_allergies(dog_id)
    allergen_names = [a.allergen_name for a in allergies]

    return VaccinationReportOut(
        dog_id=dog_id,
        dog_name=dog.name,
        breed=dog.breed.value,
        allergies=allergen_names,
        evaluations=evaluations,
    )
