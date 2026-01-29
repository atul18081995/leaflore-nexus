from django.db import models
from django.utils.text import slugify

class Plant(models.Model):
    common_name = models.CharField(
        max_length=200,
        db_index=True
    )
    scientific_name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        help_text="URL-friendly unique identifier"
    )
    family = models.CharField(
        max_length=100,
        db_index=True
    )
    genus = models.CharField(
        max_length=100,
        db_index=True
    )

    description = models.TextField()
    medicinal_uses = models.TextField(blank=True)
    growth_conditions = models.TextField(blank=True)

    # --- Minimal extensions (NEW) ---
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
        max_length=100,
        blank=True,
        help_text="e.g. upright, trailing, climbing",
    )

    origin_region = models.CharField(
        max_length=200,
        blank=True,
        help_text="Native region or origin",
    )

    primary_image = models.ImageField(
        upload_to="plants/",
        blank=True,
        null=True,
    )

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.scientific_name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["common_name"]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"