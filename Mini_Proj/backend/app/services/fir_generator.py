"""Multimodal FIR (First Information Report) Generator — Gemini Vision + allergy-aware analysis."""

import logging
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.dog import Dog
from app.models.fir import FIRRecord, UrgencyLevel
from app.services.allergy_filter import AllergyFilter
from app.ai.llm_client import generate_json_response, generate_vision_response
from app.ai.prompt_manager import PromptManager

logger = logging.getLogger("pawsitive_care.fir")


class FIRGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.allergy_filter = AllergyFilter(db)

    async def generate_fir(
        self, dog_id: int, description: str, image_data: bytes | None = None
    ) -> FIRRecord:
        # 1. Fetch dog profile
        result = await self.db.execute(
            select(Dog).where(Dog.id == dog_id)
        )
        dog = result.scalar_one_or_none()
        if not dog:
            raise ValueError(f"Dog with id {dog_id} not found")

        # 2. Query allergy constraints (ALLERGY-FIRST)
        allergy_constraint = await self.allergy_filter.get_allergy_constraint_prompt(dog_id)

        # 3. Vision analysis (if image provided)
        visual_summary = None
        if image_data:
            try:
                visual_summary = await self._analyze_image(image_data, dog.breed.value)
            except Exception as e:
                logger.error(f"Vision analysis failed: {e}")
                visual_summary = "Image analysis unavailable — proceeding with text-only assessment."

        # 4. Build FIR prompt
        prompt = PromptManager.fir_prompt(
            breed=dog.breed.value,
            age=dog.age_years,
            weight=dog.weight_kg,
            description=description,
            visual_summary=visual_summary or "No image provided",
            allergy_constraints=allergy_constraint,
        )

        # 5. Generate FIR via LLM
        try:
            report = await generate_json_response(prompt)
        except Exception as e:
            logger.error(f"FIR generation failed: {e}")
            report = self._fallback_report(description)

        # 6. Map urgency
        urgency_map = {"low": UrgencyLevel.LOW, "moderate": UrgencyLevel.MODERATE, "high": UrgencyLevel.HIGH, "critical": UrgencyLevel.CRITICAL}
        urgency = urgency_map.get(report.get("urgency", "moderate").lower(), UrgencyLevel.MODERATE)

        # 7. Persist FIR record
        fir_record = FIRRecord(
            dog_id=dog_id,
            owner_description=description,
            visual_summary=report.get("visual_summary", visual_summary),
            affected_systems=report.get("affected_systems", []),
            allergy_warnings=report.get("allergy_warnings", []),
            immediate_care=report.get("immediate_care", ""),
            urgency=urgency,
            risk_score=report.get("risk_score"),
            full_report=report,
        )
        self.db.add(fir_record)
        await self.db.commit()
        await self.db.refresh(fir_record)

        logger.info(f"FIR #{fir_record.id} generated for dog {dog_id} — urgency: {urgency.value}")
        return fir_record

    async def _analyze_image(self, image_data: bytes, breed: str) -> str:
        prompt = PromptManager.vision_analysis_prompt(breed)
        b64_image = base64.b64encode(image_data).decode("utf-8")
        return await generate_vision_response(prompt, b64_image)

    def _fallback_report(self, description: str) -> dict:
        return {
            "visual_summary": "AI analysis unavailable",
            "affected_systems": ["Unable to determine — consult veterinarian"],
            "allergy_warnings": [],
            "immediate_care": "Monitor closely and consult a licensed veterinarian immediately if symptoms worsen.",
            "urgency": "moderate",
            "risk_score": 50.0,
        }
