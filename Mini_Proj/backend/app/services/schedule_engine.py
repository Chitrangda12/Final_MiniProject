"""Smart outdoor scheduling engine using lightweight ML clustering."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

import httpx
from sklearn.cluster import KMeans
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.dog import Dog
from app.services.allergy_filter import AllergyFilter

logger = logging.getLogger("pawsitive_care.schedule")
settings = get_settings()


class SmartOutdoorScheduleEngine:
    """Generates slot-wise outdoor recommendations using ML + allergy constraints."""

    SLOT_ORDER = ("Morning", "Afternoon", "Evening", "Night")
    SLOT_RANGES = {
        "Morning": "6-9 AM",
        "Afternoon": "12-3 PM",
        "Evening": "5-8 PM",
        "Night": "9-11 PM",
    }
    SLOT_DELTAS = {
        "Morning": {"aqi": -10, "temp": -3, "humidity": +4, "pollen": -1},
        "Afternoon": {"aqi": +12, "temp": +5, "humidity": -6, "pollen": +1},
        "Evening": {"aqi": +4, "temp": -1, "humidity": +2, "pollen": 0},
        "Night": {"aqi": -4, "temp": -6, "humidity": +6, "pollen": -1},
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.allergy_filter = AllergyFilter(db)
        self._cache: dict[str, float | str] = {
            "aqi": 70.0,
            "temp": 25.0,
            "humidity": 60.0,
            "pollen": "Medium",
        }

    async def generate_schedule(
        self,
        dog_id: int,
        location: str,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict:
        dog = await self._get_dog(dog_id)
        env_allergies = await self.allergy_filter.get_environmental_allergies(dog_id)
        baseline = await self._fetch_environment_baseline(latitude, longitude)
        slots = self._build_slot_conditions(baseline)

        schedule: list[dict[str, str]] = []
        for slot in slots:
            base_risk = self._predict_risk(slot)
            adjusted_risk = self._apply_allergy_constraints(base_risk, slot, env_allergies)
            risk_label = self._risk_label(adjusted_risk)
            schedule.append(
                {
                    "time_slot": slot["time_slot"],
                    "risk_level": risk_label,
                    "recommendation": self._recommendation_for(risk_label, slot["pollen"]),
                }
            )

        return {
            "dog_id": dog_id,
            "dog_name": dog.name,
            "location": location,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schedule": schedule,
        }

    async def _get_dog(self, dog_id: int) -> Dog:
        result = await self.db.execute(select(Dog).where(Dog.id == dog_id))
        dog = result.scalar_one_or_none()
        if not dog:
            raise ValueError(f"Dog with id {dog_id} not found")
        return dog

    async def _fetch_environment_baseline(
        self, latitude: float | None, longitude: float | None
    ) -> dict[str, float | str]:
        lat = latitude if latitude is not None else 28.6139
        lng = longitude if longitude is not None else 77.2090

        try:
            weather_task = self._fetch_weather(lat, lng)
            aqi_task = self._fetch_aqi(lat, lng)
            weather, aqi = await asyncio.wait_for(
                asyncio.gather(weather_task, aqi_task), timeout=2.4
            )
            pollen = self._estimate_pollen(weather["temp"], weather["humidity"])

            self._cache = {
                "aqi": float(aqi["aqi"]),
                "temp": float(weather["temp"]),
                "humidity": float(weather["humidity"]),
                "pollen": pollen,
            }
            return self._cache.copy()
        except Exception as exc:
            logger.warning(f"Using cached/static environment baseline due to fetch error: {exc}")
            return self._cache.copy()

    async def _fetch_weather(self, lat: float, lng: float) -> dict[str, float]:
        if not settings.OPENWEATHER_API_KEY:
            return {"temp": 25.0, "humidity": 60.0}

        async with httpx.AsyncClient(timeout=1.2) as client:
            resp = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"lat": lat, "lon": lng, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"},
            )
            data = resp.json()
            return {
                "temp": float(data.get("main", {}).get("temp", 25.0)),
                "humidity": float(data.get("main", {}).get("humidity", 60.0)),
            }

    async def _fetch_aqi(self, lat: float, lng: float) -> dict[str, float]:
        if not settings.AQI_API_KEY:
            return {"aqi": 70.0}

        async with httpx.AsyncClient(timeout=1.2) as client:
            resp = await client.get(
                f"https://api.waqi.info/feed/geo:{lat};{lng}/",
                params={"token": settings.AQI_API_KEY},
            )
            data = resp.json()
            return {"aqi": float(data.get("data", {}).get("aqi", 70.0))}

    def _estimate_pollen(self, temp: float, humidity: float) -> str:
        if temp >= 30 or humidity >= 78:
            return "High"
        if temp >= 23 or humidity >= 55:
            return "Medium"
        return "Low"

    def _build_slot_conditions(self, baseline: dict[str, float | str]) -> list[dict[str, float | str]]:
        slots: list[dict[str, float | str]] = []
        for slot_name in self.SLOT_ORDER:
            delta = self.SLOT_DELTAS[slot_name]
            pollen_numeric = max(0, min(2, self._encode_pollen(str(baseline["pollen"])) + delta["pollen"]))
            slots.append(
                {
                    "time_slot": slot_name,
                    "time_range": self.SLOT_RANGES[slot_name],
                    "aqi": max(5.0, float(baseline["aqi"]) + float(delta["aqi"])),
                    "temp": max(-5.0, float(baseline["temp"]) + float(delta["temp"])),
                    "humidity": max(10.0, min(99.0, float(baseline["humidity"]) + float(delta["humidity"]))),
                    "pollen": self._decode_pollen(pollen_numeric),
                }
            )
        return slots

    def _predict_risk(self, slot: dict[str, float | str]) -> int:
        features = [
            [
                float(slot["aqi"]),
                float(slot["temp"]),
                float(slot["humidity"]),
                float(self._encode_pollen(str(slot["pollen"]))),
            ]
        ]
        cluster_id = int(_MODEL.predict(features)[0])
        return int(_CLUSTER_RISK_MAP[cluster_id])

    def _apply_allergy_constraints(
        self, risk: int, slot: dict[str, float | str], env_allergies: list[str]
    ) -> int:
        if not env_allergies:
            return risk

        adjusted = risk + 1
        pollen_related = {"pollen", "grass", "ragweed", "tree pollen"}
        humidity_related = {"dust mites", "mold"}
        allergies_set = {a.lower() for a in env_allergies}

        if str(slot["pollen"]).lower() == "high" and allergies_set.intersection(pollen_related):
            adjusted += 1
        if float(slot["humidity"]) >= 80 and allergies_set.intersection(humidity_related):
            adjusted += 1

        return min(adjusted, 2)

    def _risk_label(self, risk_value: int) -> str:
        return {0: "Safe", 1: "Moderate", 2: "Unsafe"}.get(risk_value, "Moderate")

    def _recommendation_for(self, risk_label: str, pollen_level: str) -> str:
        if risk_label == "Safe":
            return "Best time for outdoor activity"
        if risk_label == "Moderate":
            return f"Short supervised walk only; pollen is {pollen_level.lower()}"
        return "Avoid outdoor exposure"

    def _encode_pollen(self, pollen: str) -> int:
        return {"low": 0, "medium": 1, "high": 2}.get(pollen.strip().lower(), 1)

    def _decode_pollen(self, value: int) -> str:
        return {0: "Low", 1: "Medium", 2: "High"}.get(value, "Medium")


def _train_kmeans_model() -> tuple[KMeans, dict[int, int]]:
    """Train a tiny synthetic KMeans model and map clusters to risk classes."""
    synthetic_samples = [
        [25, 20, 45, 0], [35, 22, 50, 0], [45, 24, 55, 1], [55, 26, 58, 1],
        [70, 28, 62, 1], [85, 30, 65, 1], [95, 32, 70, 2], [110, 33, 74, 2],
        [130, 34, 78, 2], [145, 35, 80, 2], [60, 21, 85, 1], [90, 29, 82, 2],
        [40, 18, 88, 1], [20, 16, 60, 0], [75, 31, 67, 2], [50, 23, 52, 1],
    ]

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    model.fit(synthetic_samples)

    # Convert unsupervised clusters into ordered risk classes by centroid severity.
    centroids = model.cluster_centers_
    centroid_risk = {}
    for idx, center in enumerate(centroids):
        aqi, temp, humidity, pollen = center
        score = (aqi / 50.0) + (temp / 20.0) + (humidity / 40.0) + (pollen * 1.2)
        centroid_risk[idx] = score

    sorted_clusters = sorted(centroid_risk, key=centroid_risk.get)
    cluster_to_risk = {
        sorted_clusters[0]: 0,  # Safe
        sorted_clusters[1]: 1,  # Moderate
        sorted_clusters[2]: 2,  # Unsafe
    }
    return model, cluster_to_risk


_MODEL, _CLUSTER_RISK_MAP = _train_kmeans_model()
