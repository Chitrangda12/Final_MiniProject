from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.fir_generator import FIRGenerator
from app.schemas.fir import FIROut

router = APIRouter(prefix="/api/v1/fir", tags=["FIR"])


@router.post("/generate", response_model=FIROut)
async def generate_fir(
    dog_id: int = Form(...),
    description: str = Form(..., min_length=10),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_data = None
    if image:
        image_data = await image.read()

    generator = FIRGenerator(db)
    try:
        fir_record = await generator.generate_fir(dog_id, description, image_data)
        return fir_record
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FIR generation failed: {str(e)}")
