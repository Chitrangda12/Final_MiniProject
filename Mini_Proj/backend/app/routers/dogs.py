from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.dog import Dog
from app.models.allergy import Allergy
from sqlalchemy.orm import selectinload
from app.schemas.dog import DogCreate, DogUpdate, DogOut, DogListOut

router = APIRouter(prefix="/api/v1/dogs", tags=["Dogs"])


@router.post("/", response_model=DogOut, status_code=201)
async def create_dog(data: DogCreate, db: AsyncSession = Depends(get_db)):
    dog = Dog(**data.model_dump())
    db.add(dog)
    await db.commit()
    
    # Eager load the required relationships for serialization
    result = await db.execute(
        select(Dog).options(selectinload(Dog.allergies)).where(Dog.id == dog.id)
    )
    return result.scalar_one()


@router.get("/", response_model=DogListOut)
async def list_dogs(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    count_result = await db.execute(select(func.count(Dog.id)))
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Dog)
        .options(selectinload(Dog.allergies))
        .offset(skip)
        .limit(limit)
        .order_by(Dog.created_at.desc())
    )
    dogs = result.scalars().all()
    return {"dogs": dogs, "total": total}


@router.get("/{dog_id}", response_model=DogOut)
async def get_dog(dog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dog)
        .options(selectinload(Dog.allergies))
        .where(Dog.id == dog_id)
    )
    dog = result.scalar_one_or_none()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    return dog


@router.put("/{dog_id}", response_model=DogOut)
async def update_dog(dog_id: int, data: DogUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dog).options(selectinload(Dog.allergies)).where(Dog.id == dog_id)
    )
    dog = result.scalar_one_or_none()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dog, key, value)

    await db.commit()
    
    # Needs a fresh select to keep eager loaded relationships intact
    result = await db.execute(
        select(Dog).options(selectinload(Dog.allergies)).where(Dog.id == dog_id)
    )
    return result.scalar_one()


@router.delete("/{dog_id}", status_code=204)
async def delete_dog(dog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dog).where(Dog.id == dog_id))
    dog = result.scalar_one_or_none()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    await db.delete(dog)
    await db.commit()
