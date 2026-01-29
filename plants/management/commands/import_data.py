from django.core.management.base import BaseCommand
from plants.models import (
    Plant,
    PlantCareProfile,
    ClimateCareOverride
)
from django.utils.text import slugify
from pathlib import Path
import pandas as pd


class Command(BaseCommand):
    help = "Import plants, plant care, and climate care CSV data"

    def handle(self, *args, **kwargs):
        base = Path("plants/data")

        self.load_plants(base / "plants.csv")
        self.load_plant_care(base / "plant_care.csv")
        self.load_climate_care(base / "climate_care.csv")

        self.stdout.write(self.style.SUCCESS("✅ All CSV data loaded successfully"))

    # --------------------------------------------------
    # 1️⃣ Plants
    # --------------------------------------------------
    def load_plants(self, file_path):
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            Plant.objects.update_or_create(
                scientific_name=row["scientific_name"],
                defaults={
                    "common_name": row["common_name"],
                    "slug": slugify(row["scientific_name"]),
                    "family": row["family"],
                    "genus": row["genus"],
                    "species": row["species"],
                    "plant_type": row["plant_type"].lower() if pd.notna(row["plant_type"]) else "",
                    "lifecycle": row["lifecycle"].lower() if pd.notna(row["lifecycle"]) else "",
                    "growth_habit": row["growth_habit"],
                    "description": row["description"],
                    "origin_region": row["origin_region"],
                    "native_range": row["native_range"],
                    "medicinal_uses": row["medicinal_uses"],
                    "agricultural_uses": row["agricultural_uses"],
                    "cultural_significance": row["cultural_significance"],
                    "toxicity": row["toxicity"],
                    "precautions": row["precautions"],
                    "is_published": bool(row["is_published"]),
                }
            )

        self.stdout.write("✔ plants.csv loaded")

    # --------------------------------------------------
    # 2️⃣ Plant Care Profile
    # --------------------------------------------------
    def load_plant_care(self, file_path):
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            try:
                plant = Plant.objects.get(scientific_name=row["scientific_name"])
            except Plant.DoesNotExist:
                continue

            PlantCareProfile.objects.update_or_create(
                plant=plant,
                defaults={
                    "light_requirement": row["light_requirement"],
                    "watering_frequency": row["watering_frequency"],
                    "soil_type": row["soil_type"],
                    "temperature_range": row["temperature_range"],
                    "humidity_preference": row["humidity_preference"],
                    "indoor_outdoor": row["indoor_outdoor"].lower(),
                    "pot_or_ground": row["pot_or_ground"].lower(),
                    "growth_speed": row["growth_speed"],
                    "expected_height": row["expected_height"],
                    "beginner_mistakes": row["beginner_mistakes"],
                    "toxicity_notes": row["toxicity_notes"],
                }
            )

        self.stdout.write("✔ plant_care.csv loaded")

    # --------------------------------------------------
    # 3️⃣ Climate Care Overrides
    # --------------------------------------------------
    def load_climate_care(self, file_path):
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            try:
                plant = Plant.objects.get(scientific_name=row["scientific_name"])
                care = plant.care
            except (Plant.DoesNotExist, PlantCareProfile.DoesNotExist):
                continue

            ClimateCareOverride.objects.update_or_create(
                care_profile=care,
                climate_zone=row["climate_zone"].lower(),
                season=row["season"].lower(),
                defaults={
                    "watering_adjustment": row["watering_adjustment"],
                    "sunlight_adjustment": row["sunlight_adjustment"],
                    "special_notes": row["special_notes"],
                }
            )

        self.stdout.write("✔ climate_care.csv loaded")