"""AI Diet Planner — breed-aware, allergy-filtered meal planning via Gemini."""

import logging
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.dog import Dog
from app.services.allergy_filter import AllergyFilter
from app.ai.llm_client import generate_json_response
from app.ai.prompt_manager import PromptManager

logger = logging.getLogger("pawsitive_care.diet")


class DietPlanner:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.allergy_filter = AllergyFilter(db)

    async def generate_meal_plan(self, dog_id: int, preferences: str | None = None) -> dict:
        # 1. Fetch dog profile
        result = await self.db.execute(select(Dog).where(Dog.id == dog_id))
        dog = result.scalar_one_or_none()
        if not dog:
            raise ValueError(f"Dog with id {dog_id} not found")

        # 2. Query allergy constraints (ALLERGY-FIRST)
        allergy_constraint = await self.allergy_filter.get_allergy_constraint_prompt(dog_id)
        food_allergens = await self.allergy_filter.get_food_allergies(dog_id)

        # 3. Build prompt
        prompt = PromptManager.diet_plan_prompt(
            breed=dog.breed.value,
            age=dog.age_years,
            weight=dog.weight_kg,
            allergy_constraints=allergy_constraint,
            preferences=preferences,
        )

        # 4. Call LLM
        try:
            response = await generate_json_response(prompt)
        except Exception as e:
            logger.error(f"LLM call failed for diet plan: {e}")
            response = self._fallback_plan(dog, food_allergens)

        # 5. Post-LLM allergy safety net
        if isinstance(response, dict) and "avoid_list" in response:
            for allergen in food_allergens:
                if allergen not in [a.lower() for a in response["avoid_list"]]:
                    response["avoid_list"].append(allergen.title())

        return {
            "dog_name": dog.name,
            "breed": dog.breed.value,
            "age_years": dog.age_years,
            "weight_kg": dog.weight_kg,
            "allergies": food_allergens,
            "meal_plan": response.get("meal_plan", {}),
            "avoid_list": response.get("avoid_list", food_allergens),
            "supplements": response.get("supplements", []),
            "feeding_schedule": response.get("feeding_schedule", {}),
            "disclaimer": "This diet plan is AI-generated guidance. Consult your veterinarian for specific dietary needs.",
        }

    def _fallback_plan(self, dog: Dog, allergens: list[str]) -> dict:
        return {
            "meal_plan": {
                "morning": "Veterinarian-recommended hypoallergenic kibble",
                "evening": "Limited ingredient diet with novel protein",
            },
            "avoid_list": [a.title() for a in allergens],
            "supplements": ["Omega-3 fatty acids", "Probiotics"],
            "feeding_schedule": {
                "meals_per_day": 2,
                "morning": "7:00 AM",
                "evening": "6:00 PM",
            },
        }
