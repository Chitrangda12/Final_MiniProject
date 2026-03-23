"""Core Allergy Constraint Engine — the heart of Pawsitive Care's safety-first architecture.

Every module MUST query this engine before generating output.
All filtering decisions are logged for audit trails.
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.allergy import Allergy, AllergyCategory

logger = logging.getLogger("pawsitive_care.allergy_filter")


class AllergyFilter:
    """Centralized allergy constraint engine for the allergy-first pipeline."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_allergies(self, dog_id: int) -> list[Allergy]:
        result = await self.db.execute(
            select(Allergy).where(Allergy.dog_id == dog_id)
        )
        return list(result.scalars().all())

    async def get_food_allergies(self, dog_id: int) -> list[str]:
        allergies = await self.get_allergies(dog_id)
        food_allergens = [
            a.allergen_name.lower()
            for a in allergies
            if a.category == AllergyCategory.FOOD
        ]
        logger.info(f"Dog {dog_id} food allergens: {food_allergens}")
        return food_allergens

    async def get_environmental_allergies(self, dog_id: int) -> list[str]:
        allergies = await self.get_allergies(dog_id)
        env_allergens = [
            a.allergen_name.lower()
            for a in allergies
            if a.category == AllergyCategory.ENVIRONMENTAL
        ]
        logger.info(f"Dog {dog_id} environmental allergens: {env_allergens}")
        return env_allergens

    async def get_medication_allergies(self, dog_id: int) -> list[str]:
        allergies = await self.get_allergies(dog_id)
        med_allergens = [
            a.allergen_name.lower()
            for a in allergies
            if a.category == AllergyCategory.MEDICATION
        ]
        logger.info(f"Dog {dog_id} medication allergens: {med_allergens}")
        return med_allergens

    def filter_items(self, items: list[str], allergens: list[str]) -> list[str]:
        """Remove items that match known allergens."""
        safe_items = []
        for item in items:
            is_safe = True
            for allergen in allergens:
                if allergen in item.lower():
                    logger.warning(f"BLOCKED: '{item}' contains allergen '{allergen}'")
                    is_safe = False
                    break
            if is_safe:
                safe_items.append(item)
        return safe_items

    async def get_allergy_constraint_prompt(self, dog_id: int) -> str:
        """Generate a constraint string for LLM prompts."""
        allergies = await self.get_allergies(dog_id)
        if not allergies:
            return "No known allergies."

        constraints = []
        for a in allergies:
            constraints.append(f"- {a.allergen_name} ({a.category.value}, severity: {a.severity.value})")

        return (
            "CRITICAL ALLERGY CONSTRAINTS — DO NOT recommend anything containing these:\n"
            + "\n".join(constraints)
        )
