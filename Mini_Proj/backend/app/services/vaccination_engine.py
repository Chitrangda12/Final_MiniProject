"""Vaccination Filtering Engine — rule-based contraindication detection."""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.allergy_filter import AllergyFilter
from app.models.vaccination import VaccineStatus

logger = logging.getLogger("pawsitive_care.vaccination")

# Contraindication matrix: vaccine → list of allergens that make it unsafe/conditional
VACCINE_CONTRAINDICATIONS: dict[str, dict[str, list[str]]] = {
    "Rabies (Imrab)": {
        "unsafe": ["neomycin", "polymyxin"],
        "conditional": ["egg"]
    },
    "DHPP (Distemper combo)": {
        "unsafe": ["neomycin", "gentamicin"],
        "conditional": ["bovine serum", "beef"]
    },
    "Bordetella (Kennel Cough)": {
        "unsafe": [],
        "conditional": ["egg"]
    },
    "Leptospirosis": {
        "unsafe": [],
        "conditional": ["thimerosal"]
    },
    "Canine Influenza (H3N2/H3N8)": {
        "unsafe": ["egg"],
        "conditional": ["mercury", "thimerosal"]
    },
    "Lyme Disease": {
        "unsafe": [],
        "conditional": ["gentamicin"]
    },
    "Parvovirus": {
        "unsafe": ["neomycin"],
        "conditional": ["bovine serum", "beef"]
    },
    "Parainfluenza": {
        "unsafe": [],
        "conditional": ["egg", "chicken"]
    },
}


class VaccinationEngine:
    def __init__(self, db: AsyncSession):
        self.allergy_filter = AllergyFilter(db)

    async def evaluate_all_vaccines(self, dog_id: int) -> list[dict]:
        all_allergens = await self.allergy_filter.get_allergies(dog_id)
        allergen_names = [a.allergen_name.lower() for a in all_allergens]

        evaluations = []
        for vaccine_name, rules in VACCINE_CONTRAINDICATIONS.items():
            status = VaccineStatus.SAFE
            matched_contraindications = []
            reason = "No known contraindications with this dog's allergy profile."

            for allergen in allergen_names:
                if allergen in [c.lower() for c in rules.get("unsafe", [])]:
                    status = VaccineStatus.UNSAFE
                    matched_contraindications.append(allergen)
                    reason = f"UNSAFE: Contains {allergen} — dog has severe allergy."
                    break
                if allergen in [c.lower() for c in rules.get("conditional", [])]:
                    if status != VaccineStatus.UNSAFE:
                        status = VaccineStatus.CONDITIONAL
                        matched_contraindications.append(allergen)
                        reason = f"CONDITIONAL: May contain {allergen}. Veterinarian supervision required."

            evaluations.append({
                "vaccine_name": vaccine_name,
                "status": status,
                "contraindications": matched_contraindications,
                "reason": reason,
            })

        logger.info(f"Vaccination evaluation for dog {dog_id}: {len(evaluations)} vaccines assessed")
        return evaluations
