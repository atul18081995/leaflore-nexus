from django.db.models import Q
from plants.models import Plant


class PlantAlternativeEngine:
    """
    Recommends alternative plants based on care profile similarity.

    Priority:
    1. Nursery sellable plants
    2. Knowledge-only plants

    This engine is schema-safe:
    - Uses ONLY fields that exist in Plant & PlantCareProfile
    - Never raises AttributeError
    """

    def __init__(self, base_plant):
        self.base_plant = base_plant
        self.base_care = getattr(base_plant, "care", None)

    def get_alternatives(self, limit=4):
        if not self.base_care:
            return []

        qs = (
            Plant.objects
            .filter(is_published=True)
            .exclude(id=self.base_plant.id)
            .select_related("care", "nursery")
        )

        # -------------------------------
        # Core similarity (SAFE fields)
        # -------------------------------
        qs = qs.filter(
            plant_type=self.base_plant.plant_type,
            care__light_requirement=self.base_care.light_requirement,
            care__watering_frequency=self.base_care.watering_frequency,
            care__indoor_outdoor=self.base_care.indoor_outdoor,
        )

        # -------------------------------
        # Priority: nursery first
        # -------------------------------
        nursery_qs = qs.filter(
            nursery__is_sellable=True
        )

        fallback_qs = qs.exclude(
            id__in=nursery_qs.values_list("id", flat=True)
        )

        alternatives = list(nursery_qs[:limit])

        if len(alternatives) < limit:
            needed = limit - len(alternatives)
            alternatives.extend(list(fallback_qs[:needed]))

        return alternatives

    # --------------------------------------------------
    # OPTIONAL: Explanation generator (SAFE)
    # --------------------------------------------------
    def get_reasons(self, alternative):
        """
        Returns human-friendly reasons why this plant is recommended.
        This NEVER breaks even if fields are missing.
        """

        reasons = []

        alt_care = getattr(alternative, "care", None)
        if not alt_care or not self.base_care:
            return reasons

        if alt_care.light_requirement == self.base_care.light_requirement:
            reasons.append("Similar light requirement")

        if alt_care.watering_frequency == self.base_care.watering_frequency:
            reasons.append("Similar watering needs")

        if alt_care.indoor_outdoor == self.base_care.indoor_outdoor:
            reasons.append("Same indoor/outdoor suitability")

        if getattr(alternative, "nursery", None) and alternative.nursery.is_sellable:
            reasons.append("Available via nursery")

        return reasons