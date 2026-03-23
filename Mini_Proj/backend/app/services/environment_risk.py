"""Environmental Risk Module — aggregates external APIs and scores risk."""

import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.dog import Dog
from app.services.allergy_filter import AllergyFilter
from app.config import get_settings

logger = logging.getLogger("pawsitive_care.environment")
settings = get_settings()


class EnvironmentRiskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.allergy_filter = AllergyFilter(db)

    async def assess_risk(self, dog_id: int, lat: float, lng: float) -> dict:
        result = await self.db.execute(select(Dog).where(Dog.id == dog_id))
        dog = result.scalar_one_or_none()
        if not dog:
            raise ValueError(f"Dog with id {dog_id} not found")

        # Query environmental allergies (ALLERGY-FIRST)
        env_allergens = await self.allergy_filter.get_environmental_allergies(dog_id)

        # Fetch external data
        weather = await self._fetch_weather(lat, lng)
        aqi = await self._fetch_aqi(lat, lng)

        # Calculate risk
        risk_score, risk_level, alerts = self._calculate_risk(weather, aqi, env_allergens)

        # Activity guidance
        guidance = self._generate_guidance(risk_level, env_allergens, weather)

        return {
            "dog_name": dog.name,
            "location": {"latitude": lat, "longitude": lng},
            "risk_score": risk_score,
            "risk_level": risk_level,
            "environmental_data": {
                "temperature": weather.get("temp"),
                "humidity": weather.get("humidity"),
                "wind_speed": weather.get("wind_speed"),
                "description": weather.get("description", "N/A"),
                "aqi": aqi.get("aqi"),
                "aqi_category": aqi.get("category", "N/A"),
            },
            "allergy_alerts": alerts,
            "activity_guidance": guidance,
            "disclaimer": "Environmental risk data is approximate. Monitor your pet and consult a vet for unusual symptoms.",
        }

    async def _fetch_weather(self, lat: float, lng: float) -> dict:
        if not settings.OPENWEATHER_API_KEY:
            return {"temp": 25, "humidity": 60, "wind_speed": 10, "description": "Mock data — set OPENWEATHER_API_KEY"}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={"lat": lat, "lon": lng, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"},
                )
                data = resp.json()
                return {
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "description": data["weather"][0]["description"],
                }
        except Exception as e:
            logger.error(f"Weather API failed: {e}")
            return {"temp": 25, "humidity": 60, "wind_speed": 10, "description": "API unavailable"}

    async def _fetch_aqi(self, lat: float, lng: float) -> dict:
        if not settings.AQI_API_KEY:
            return {"aqi": 50, "category": "Moderate (mock data — set AQI_API_KEY)"}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"https://api.waqi.info/feed/geo:{lat};{lng}/",
                    params={"token": settings.AQI_API_KEY},
                )
                data = resp.json()
                aqi_val = data.get("data", {}).get("aqi", 50)
                return {"aqi": aqi_val, "category": self._aqi_category(aqi_val)}
        except Exception as e:
            logger.error(f"AQI API failed: {e}")
            return {"aqi": 50, "category": "Unknown"}

    def _aqi_category(self, aqi: int) -> str:
        if aqi <= 50: return "Good"
        if aqi <= 100: return "Moderate"
        if aqi <= 150: return "Unhealthy for Sensitive Groups"
        if aqi <= 200: return "Unhealthy"
        if aqi <= 300: return "Very Unhealthy"
        return "Hazardous"

    def _calculate_risk(self, weather: dict, aqi: dict, allergens: list[str]) -> tuple[float, str, list[str]]:
        score = 0.0
        alerts = []

        # Temperature risk
        temp = weather.get("temp", 25)
        if temp > 35:
            score += 30
            alerts.append("⚠️ Extreme heat — limit outdoor activity")
        elif temp > 30:
            score += 15
            alerts.append("🌡️ High temperature — ensure hydration")

        # Humidity risk (affects skin allergies)
        humidity = weather.get("humidity", 50)
        if humidity > 80:
            score += 15
            if any(a in ["dust mites", "mold"] for a in allergens):
                score += 20
                alerts.append("🌧️ High humidity + dust mite/mold allergy — keep indoors")

        # AQI risk
        aqi_val = aqi.get("aqi", 50)
        if aqi_val > 150:
            score += 25
            alerts.append("🏭 Poor air quality — avoid outdoor exercise")
        elif aqi_val > 100:
            score += 10
            alerts.append("💨 Moderate air quality — limit prolonged outdoor activity")

        # Pollen season alert for grass/pollen allergies
        if any(a in ["pollen", "grass", "ragweed", "tree pollen"] for a in allergens):
            score += 15
            alerts.append("🌾 Pollen/grass allergy detected — check local pollen count before walks")

        score = min(score, 100)
        level = "low" if score < 30 else "moderate" if score < 60 else "high" if score < 80 else "critical"

        return round(score, 1), level, alerts

    def _generate_guidance(self, risk_level: str, allergens: list[str], weather: dict) -> list[dict]:
        guidance = []

        if risk_level in ["high", "critical"]:
            guidance.append({
                "activity": "Outdoor walks",
                "recommendation": "Limit to 10-15 minutes, early morning or late evening",
                "icon": "🚶"
            })
            guidance.append({
                "activity": "Indoor play",
                "recommendation": "Preferred — use indoor enrichment toys",
                "icon": "🏠"
            })
        else:
            guidance.append({
                "activity": "Outdoor walks",
                "recommendation": "Normal duration, monitor for symptoms",
                "icon": "🚶"
            })

        if any(a in ["pollen", "grass"] for a in allergens):
            guidance.append({
                "activity": "Post-walk care",
                "recommendation": "Wipe paws and coat after outdoor activity",
                "icon": "🧹"
            })

        if weather.get("temp", 25) > 30:
            guidance.append({
                "activity": "Hydration",
                "recommendation": "Ensure fresh water available at all times",
                "icon": "💧"
            })

        return guidance
