"""Centralized Prompt Manager — all LLM prompts live here to prevent prompt drift."""


class PromptManager:
    @staticmethod
    def diet_plan_prompt(
        breed: str, age: float, weight: float,
        allergy_constraints: str, preferences: str | None = None,
    ) -> str:
        pref_line = f"\nOwner Preferences: {preferences}" if preferences else ""
        return f"""You are a veterinary nutritionist AI assistant. Generate a personalized diet plan for a dog.

DOG PROFILE:
- Breed: {breed}
- Age: {age} years
- Weight: {weight} kg
{pref_line}

{allergy_constraints}

IMPORTANT RULES:
1. NEVER include any ingredient that matches the allergy constraints above.
2. Consider breed-specific nutritional needs.
3. Provide practical, actionable meal plans.
4. Include supplements appropriate for the breed and age.

Respond ONLY with valid JSON in this exact format:
{{
  "meal_plan": {{
    "morning": "description of morning meal",
    "evening": "description of evening meal",
    "snacks": "description of safe snack options"
  }},
  "avoid_list": ["allergen1", "allergen2"],
  "supplements": ["supplement1", "supplement2"],
  "feeding_schedule": {{
    "meals_per_day": 2,
    "morning": "7:00 AM",
    "evening": "6:00 PM",
    "notes": "any special instructions"
  }}
}}"""

    @staticmethod
    def fir_prompt(
        breed: str, age: float, weight: float,
        description: str, visual_summary: str,
        allergy_constraints: str,
    ) -> str:
        return f"""You are a veterinary triage AI assistant. Generate a First Information Report (FIR) for a dog health concern.

DOG PROFILE:
- Breed: {breed}
- Age: {age} years
- Weight: {weight} kg

OWNER'S DESCRIPTION:
{description}

VISUAL ANALYSIS:
{visual_summary}

{allergy_constraints}

IMPORTANT RULES:
1. Do NOT provide a medical diagnosis.
2. Do NOT prescribe medication.
3. Consider breed-specific health predispositions.
4. Flag any allergy-related concerns.
5. Always recommend consulting a licensed veterinarian.

Respond ONLY with valid JSON in this exact format:
{{
  "visual_summary": "summary of visual observations",
  "affected_systems": ["system1", "system2"],
  "allergy_warnings": ["warning1 if applicable"],
  "immediate_care": "safe first-aid advice",
  "urgency": "low|moderate|high|critical",
  "risk_score": 0-100,
  "breed_considerations": "breed-specific notes",
  "recommended_action": "what the owner should do next"
}}"""

    @staticmethod
    def vision_analysis_prompt(breed: str) -> str:
        return f"""Analyze this image of a {breed} dog. Describe:
1. Any visible symptoms or abnormalities (skin, eyes, posture, coat)
2. General condition assessment
3. Any areas of concern

Be factual and objective. Do NOT diagnose. Just describe what you observe."""
