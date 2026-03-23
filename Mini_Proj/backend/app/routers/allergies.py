from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.allergy import Allergy
from app.models.dog import Dog
from app.schemas.allergy import AllergyCreate, AllergyOut, AllergyBulkCreate, AllergyUpdate

router = APIRouter(prefix="/api/v1/dogs/{dog_id}/allergies", tags=["Allergies"])


@router.get("/", response_model=list[AllergyOut])
async def list_allergies(dog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Allergy).where(Allergy.dog_id == dog_id))
    return result.scalars().all()


@router.post("/", response_model=AllergyOut, status_code=201)
async def add_allergy(dog_id: int, data: AllergyCreate, db: AsyncSession = Depends(get_db)):
    # Verify dog exists
    dog_result = await db.execute(select(Dog).where(Dog.id == dog_id))
    if not dog_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Dog not found")

    allergy = Allergy(dog_id=dog_id, **data.model_dump())
    db.add(allergy)
    await db.commit()
    await db.refresh(allergy)
    return allergy


@router.post("/bulk", response_model=list[AllergyOut], status_code=201)
async def bulk_add_allergies(dog_id: int, data: AllergyBulkCreate, db: AsyncSession = Depends(get_db)):
    dog_result = await db.execute(select(Dog).where(Dog.id == dog_id))
    if not dog_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Dog not found")

    created = []
    for allergy_data in data.allergies:
        allergy = Allergy(dog_id=dog_id, **allergy_data.model_dump())
        db.add(allergy)
        created.append(allergy)

    await db.commit()
    for a in created:
        await db.refresh(a)
    return created


@router.put("/{allergy_id}", response_model=AllergyOut)
async def update_allergy(dog_id: int, allergy_id: int, data: AllergyUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Allergy).where(Allergy.id == allergy_id, Allergy.dog_id == dog_id)
    )
    allergy = result.scalar_one_or_none()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(allergy, key, value)

    await db.commit()
    await db.refresh(allergy)
    return allergy


@router.delete("/{allergy_id}", status_code=204)
async def delete_allergy(dog_id: int, allergy_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Allergy).where(Allergy.id == allergy_id, Allergy.dog_id == dog_id)
    )
    allergy = result.scalar_one_or_none()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")

    await db.delete(allergy)
    await db.commit()
