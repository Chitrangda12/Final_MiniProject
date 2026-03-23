from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.environment_risk import EnvironmentRiskService
from app.services.schedule_engine import SmartOutdoorScheduleEngine
from app.schemas.environment import (
    EnvironmentRiskRequest,
    EnvironmentRiskOut,
    OutdoorScheduleRequest,
    OutdoorScheduleOut,
)

router = APIRouter(prefix="/api/v1/environment", tags=["Environment"])


@router.post("/risk", response_model=EnvironmentRiskOut)
async def assess_environment_risk(data: EnvironmentRiskRequest, db: AsyncSession = Depends(get_db)):
    service = EnvironmentRiskService(db)
    try:
        result = await service.assess_risk(data.dog_id, data.latitude, data.longitude)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")


@router.post("/schedule", response_model=OutdoorScheduleOut)
async def get_outdoor_schedule(data: OutdoorScheduleRequest, db: AsyncSession = Depends(get_db)):
    service = SmartOutdoorScheduleEngine(db)
    try:
        return await service.generate_schedule(
            dog_id=data.dog_id,
            location=data.location,
            latitude=data.latitude,
            longitude=data.longitude,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schedule generation failed: {str(e)}")
