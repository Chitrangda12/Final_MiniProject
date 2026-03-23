from pydantic import BaseModel


class DietRequest(BaseModel):
    dog_id: int
    preferences: str | None = None


class MealPlanOut(BaseModel):
    dog_name: str
    breed: str
    age_years: float
    weight_kg: float
    allergies: list[str]
    meal_plan: dict
    avoid_list: list[str]
    supplements: list[str]
    feeding_schedule: dict
    disclaimer: str = "This diet plan is AI-generated guidance. Consult your veterinarian for specific dietary needs."
