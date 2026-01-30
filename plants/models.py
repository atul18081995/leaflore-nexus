from django.db import models
from django.utils.text import slugify


# =====================================================
# Plant (Core Botanical Knowledge)
# =====================================================
class Plant(models.Model):

    # -----------------
    # Identity
    # -----------------
    common_name = models.CharField(max_length=200, db_index=True)
    scientific_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        max_length=220,
        unique=True,
        help_text="URL-friendly unique identifier"
    )

    family = models.CharField(max_length=100, db_index=True)
    genus = models.CharField(max_length=100, db_index=True)
    species = models.CharField(max_length=100, blank=True)

    # -----------------
    # Classification
    # -----------------
    plant_type = models.CharField(
        max_length=50,
        choices=[
            ("tree", "Tree"),
            ("shrub", "Shrub"),
            ("herb", "Herb"),
            ("succulent", "Succulent"),
            ("climber", "Climber"),
            ("creeper", "Creeper"),
            ("aquatic", "Aquatic"),
            ("fungal", "Fungal"),
        ],
        blank=True,
    )

    lifecycle = models.CharField(
        max_length=50,
        choices=[
            ("annual", "Annual"),
            ("biennial", "Biennial"),
            ("perennial", "Perennial"),
        ],
        blank=True,
    )

    growth_habit = models.CharField(
        max_length=150,
        blank=True,
        help_text="Upright, spreading, trailing, climbing, etc."
    )

    # -----------------
    # Morphology
    # -----------------
    height = models.CharField(max_length=100, blank=True)
    canopy_spread = models.CharField(max_length=100, blank=True)

    leaf_description = models.TextField(blank=True)
    flower_description = models.TextField(blank=True)
    fruit_description = models.TextField(blank=True)
    bark_description = models.TextField(blank=True)

    # -----------------
    # Origin & Ecology
    # -----------------
    origin_region = models.CharField(
        max_length=200,
        blank=True,
        help_text="Native region or origin"
    )

    native_range = models.TextField(blank=True)

    # -----------------
    # Uses
    # -----------------
    description = models.TextField(
        help_text="General botanical overview"
    )

    medicinal_uses = models.TextField(blank=True)
    agricultural_uses = models.TextField(blank=True)
    cultural_significance = models.TextField(blank=True)

    # -----------------
    # Safety
    # -----------------
    toxicity = models.TextField(blank=True)
    precautions = models.TextField(blank=True)

    # -----------------
    # Media
    # -----------------
    primary_image = models.ImageField(
        upload_to="plants/",
        blank=True,
        null=True,
    )

    # -----------------
    # Meta
    # -----------------
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.scientific_name)
        super().save(*args, **kwargs)

    @property
    def has_nursery(self):
        return hasattr(self, "nursery")
    class Meta:
        ordering = ["common_name"]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"


# =====================================================
# Plant Images
# =====================================================
class PlantImage(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="plants/gallery/")
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.plant.common_name} image"


# =====================================================
# Plant Care Profile (HOW TO GROW)
# =====================================================
class PlantCareProfile(models.Model):

    # ✅ NEW: controlled choices (THIS FIXES YOUR ISSUE)
    INDOOR_OUTDOOR_CHOICES = [
        ("indoor", "Indoor"),
        ("outdoor", "Outdoor"),
        ("both", "Both"),
    ]

    POT_GROUND_CHOICES = [
        ("pot", "Pot"),
        ("ground", "Ground"),
        ("both", "Both"),
    ]

    plant = models.OneToOneField(
        Plant,
        on_delete=models.CASCADE,
        related_name="care"
    )

    # Light
    light_requirement = models.CharField(max_length=50)

    # Water
    watering_frequency = models.CharField(max_length=100)
    overwatering_signs = models.TextField(blank=True)
    underwatering_signs = models.TextField(blank=True)

    # Soil & Climate
    soil_type = models.CharField(max_length=100)
    temperature_range = models.CharField(max_length=50)
    humidity_preference = models.CharField(max_length=50, blank=True)

    # -----------------
    # Placement (FIXED)
    # -----------------
    indoor_outdoor = models.CharField(
        max_length=20,
        choices=INDOOR_OUTDOOR_CHOICES
    )

    pot_or_ground = models.CharField(
        max_length=20,
        choices=POT_GROUND_CHOICES
    )

    # Growth
    growth_speed = models.CharField(max_length=50, blank=True)
    expected_height = models.CharField(max_length=50, blank=True)

    # Warnings
    beginner_mistakes = models.TextField(blank=True)
    toxicity_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Care profile for {self.plant.common_name}"


# =====================================================
# Climate-based Overrides
# =====================================================
class ClimateCareOverride(models.Model):

    CLIMATE_CHOICES = [
        ("tropical", "Tropical"),
        ("subtropical", "Subtropical"),
        ("arid", "Arid"),
        ("temperate", "Temperate"),
    ]

    SEASON_CHOICES = [
        ("summer", "Summer"),
        ("monsoon", "Monsoon"),
        ("winter", "Winter"),
    ]

    care_profile = models.ForeignKey(
        PlantCareProfile,
        on_delete=models.CASCADE,
        related_name="climate_overrides"
    )

    climate_zone = models.CharField(max_length=20, choices=CLIMATE_CHOICES)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)

    watering_adjustment = models.TextField()
    sunlight_adjustment = models.TextField(blank=True)
    special_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("care_profile", "climate_zone", "season")

    def __str__(self):
        return f"{self.care_profile.plant.common_name} – {self.climate_zone} ({self.season})"