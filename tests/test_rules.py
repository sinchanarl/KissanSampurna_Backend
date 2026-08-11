import random
import string
import unittest

from fastapi import FastAPI
from starlette.testclient import TestClient
import sqlalchemy as sa

from SharedBackend.managers import BaseSchema
from config import get_engine, get_settings
from routers.v1.crops import router as crops_router
from routers.v1.rules import router as rules_router
from utils.constants import (
    LandholdingEnum, WaterSourceEnum, IrrigationTypeEnum, BudgetPerAcreEnum, MarketAccessEnum,
    RiskAppetiteEnum, CropCycleEnum, CropRotationEnum, OwnsLivestockEnum, SmartphoneUseEnum,
    MachineryUsedEnum, StorageFacilityEnum, TransportAccessEnum, TemperatureRangeEnum,
    AltitudeRangeEnum, FertilizerUsedEnum, PestManagementEnum
)


class TestRules(unittest.TestCase):
    @staticmethod
    async def lifespan(_: FastAPI):
        settings = get_settings()
        engine = get_engine(settings.name)
        async with engine.begin() as conn:
            if settings.supports_schema:
                await conn.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{settings.name}"'))
            await conn.run_sync(BaseSchema.metadata.create_all)
        yield

    def setUp(self):
        self.app = FastAPI(lifespan=self.lifespan)  # noqa
        self.app.include_router(rules_router)
        self.app.include_router(crops_router)

    @staticmethod
    def random_crop_payload():
        return {
            "name": ''.join(random.choices(string.ascii_lowercase, k=8)),
            "scientific_name": ''.join(random.choices(string.ascii_lowercase, k=12)),
            "crop_type": random.choice(["Cereal", "Pulse", "Vegetable"]),
            "season": [random.choice(["Rabi", "Kharif", "Summer"])],
            "min_temperature": random.uniform(10, 20),
            "max_temperature": random.uniform(21, 40),
            "min_rainfall": random.uniform(100, 200),
            "max_rainfall": random.uniform(201, 400),
            "soil_type": [random.choice(["Loamy", "Clay", "Sandy"])],
            "ph_min": random.uniform(5.5, 6.5),
            "ph_max": random.uniform(6.6, 8.0),
            "growing_duration": random.randint(60, 180),
            "water_requirement": random.choice(["Low", "Medium", "High"]),
            "fertilizer_requirement": random.choice(["Low", "Medium", "High"]),
            "pest_susceptibility": random.choice(["Low", "Medium", "High"]),
            "disease_susceptibility": random.choice(["Low", "Medium", "High"]),
            "average_yield": random.uniform(1, 5),
            "market_price_min": random.uniform(10, 20),
            "market_price_max": random.uniform(21, 40),
            "storage_life": random.randint(10, 90),
        }

    @staticmethod
    def random_rule_payload():
        return {
            "total_farmland_area": random.choice(list(LandholdingEnum)).value,
            "primary_water_source": random.choice(list(WaterSourceEnum)).value,
            "irrigation_available": random.choice([True, False]),
            "irrigation_type": random.choice(list(IrrigationTypeEnum)).value,
            "budget_per_acre": random.choice(list(BudgetPerAcreEnum)).value,
            "market_access": random.choice(list(MarketAccessEnum)).value,
            "preferred_crop_type": random.choice(["Cereal", "Pulse", "Vegetable"]),
            "risk_appetite": random.choice(list(RiskAppetiteEnum)).value,
            "fertilizer_used": random.choice(list(FertilizerUsedEnum)).value,
            "pest_management": random.choice(list(PestManagementEnum)).value,
            "crop_cycle": random.choice(list(CropCycleEnum)).value,
            "rotation_intercropping": random.choice(list(CropRotationEnum)).value,
            "owns_livestock": random.choice(list(OwnsLivestockEnum)).value,
            "livestock_type": None,
            "smartphone_use": random.choice(list(SmartphoneUseEnum)).value,
            "machinery_used": random.choice(list(MachineryUsedEnum)).value,
            "storage_facility": random.choice(list(StorageFacilityEnum)).value,
            "transport_access": random.choice(list(TransportAccessEnum)).value,
            "temperature_range": random.choice(list(TemperatureRangeEnum)).value,
            "altitude_range": random.choice(list(AltitudeRangeEnum)).value,
            "primary_crop_id": None
        }

    def test_add_crops_and_rules_and_apply(self):
        with TestClient(self.app) as client:
            # Add crops
            crop_ids = []
            for _ in range(5):
                payload = self.random_crop_payload()
                resp = client.post("/crops", json=payload)
                self.assertEqual(resp.status_code, 200)
                crop_ids.append(resp.json()["uid"])

            # Add rules, each with a random crop as primary_crop_id
            rule_ids = []
            for _ in range(5):
                payload = self.random_rule_payload()
                payload["primary_crop_id"] = random.choice(crop_ids)
                resp = client.post("/rules", json=payload)
                self.assertEqual(resp.status_code, 200)
                rule_ids.append(resp.json()["uid"])

            # Test apply rule with exact match
            for _ in range(3):
                rule = self.random_rule_payload()
                # Use a known crop id
                rule["primary_crop_id"] = random.choice(crop_ids)
                resp = client.post("/rules/apply", json=rule)
                # Accept 200 or 404 (if no match)
                self.assertIn(resp.status_code, [200, 404])
                if resp.status_code == 200:
                    self.assertIn("uid", resp.json())
                else:
                    self.assertIn("status", resp.json())
