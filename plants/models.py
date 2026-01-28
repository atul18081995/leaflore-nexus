from django.db import models


class Plant(models.Model):
    common_name = models.CharField(
        max_length=200,
        db_index=True
    )
    scientific_name = models.CharField(
        max_length=200,
        unique=True
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

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["common_name"]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"