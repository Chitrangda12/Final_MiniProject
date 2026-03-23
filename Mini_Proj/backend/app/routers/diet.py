from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.diet_planner import DietPlanner
from app.schemas.diet import DietRequest, MealPlanOut

router = APIRouter(prefix="/api/v1/diet", tags=["Diet"])


@router.post("/plan", response_model=MealPlanOut)
async def generate_diet_plan(data: DietRequest, db: AsyncSession = Depends(get_db)):
    planner = DietPlanner(db)
    try:
        result = await planner.generate_meal_plan(data.dog_id, data.preferences)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diet plan generation failed: {str(e)}")
