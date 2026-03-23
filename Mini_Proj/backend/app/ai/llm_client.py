"""Gemini LLM Client — wrapper for Google Generative AI."""

import json
import logging
import google.generativeai as genai
from app.config import get_settings

logger = logging.getLogger("pawsitive_care.llm")
settings = get_settings()

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


async def generate_json_response(prompt: str) -> dict:
    """Generate a structured JSON response from Gemini."""
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set — returning mock response")
        return _mock_response(prompt)

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON: {e}")
        return {"error": "Failed to parse AI response", "raw": text[:500]}
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return _mock_response(prompt)


async def generate_vision_response(prompt: str, b64_image: str) -> str:
    """Generate a vision analysis from Gemini multimodal model."""
    if not settings.GEMINI_API_KEY:
        return "Mock vision response — set GEMINI_API_KEY for real analysis."

    try:
        import base64
        image_bytes = base64.b64decode(b64_image)

        model = genai.GenerativeModel(settings.GEMINI_VISION_MODEL)
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
        return response.text.strip()
    except Exception as e:
        logger.error(f"Vision API error: {e}")
        return "Vision analysis failed — proceeding with text-only assessment."


def _mock_response(prompt: str) -> dict:
    """Fallback mock response when API key is not configured."""
    if "diet" in prompt.lower():
        return {
            "meal_plan": {
                "morning": "Hypoallergenic kibble with fish-based protein",
                "evening": "Limited ingredient wet food (duck or venison based)",
                "snacks": "Dehydrated sweet potato chews, blueberries"
            },
            "avoid_list": ["Chicken", "Beef", "Wheat", "Soy"],
            "supplements": ["Omega-3 fish oil", "Glucosamine", "Probiotics"],
            "feeding_schedule": {
                "meals_per_day": 2,
                "morning": "7:00 AM",
                "evening": "6:00 PM",
                "notes": "Always provide fresh water. Monitor stool quality."
            }
        }
    return {
        "visual_summary": "AI analysis (mock mode — set GEMINI_API_KEY)",
        "affected_systems": ["Dermatological", "General wellness"],
        "allergy_warnings": ["Review known allergens"],
        "immediate_care": "Monitor closely. Keep the area clean. Consult veterinarian.",
        "urgency": "moderate",
        "risk_score": 45.0,
        "breed_considerations": "Breed-specific assessment requires API key",
        "recommended_action": "Schedule a veterinary consultation within 48 hours."
    }
