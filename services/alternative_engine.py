from django.db.models import Q
from plants.models import Plant


class PlantAlternativeEngine:
    """
    Recommends alternative plants based on care, type, and availability.
    Priority:
    1. Nursery sellable plants
    2. Knowledge-only plants
    """

    def __init__(self, base_plant):
        self.base_plant = base_plant
        self.base_care = getattr(base_plant, "care", None)

    def get_alternatives(self, limit=4):
        if not self.base_care:
            return []

        qs = Plant.objects.filter(
            is_published=True
        ).exclude(id=self.base_plant.id)

        # --- Core similarity filters ---
        qs = qs.filter(
            plant_type=self.base_plant.plant_type
        )

        qs = qs.filter(
            care__light_requirement=self.base_care.light_requirement,
            care__watering_frequency=self.base_care.watering_frequency,
        )

        # --- Annotate nursery preference ---
        nursery_qs = qs.filter(
            nursery__is_sellable=True
        ).select_related("nursery")

        fallback_qs = qs.exclude(
            id__in=nursery_qs.values_list("id", flat=True)
        )

        # --- Combine with priority ---
        alternatives = list(nursery_qs[:limit])

        if len(alternatives) < limit:
            needed = limit - len(alternatives)
            alternatives.extend(list(fallback_qs[:needed]))

        return alternatives