from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "common_name",
        "scientific_name",
        "family",
        "genus",
        "is_published",
        "created_at",
    )

    search_fields = (
        "common_name",
        "scientific_name",
        "family",
        "genus",
    )

    list_filter = (
        "family",
        "genus",
        "is_published",
    )