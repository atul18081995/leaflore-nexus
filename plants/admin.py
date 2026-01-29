from django.contrib import admin
from django.utils.html import format_html
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "common_name",
        "scientific_name",
        "plant_type",
        "is_published",
        "image_preview",
        "created_at",
    )

    search_fields = (
        "common_name",
        "scientific_name",
        "family",
        "genus",
        "origin_region",
    )

    list_filter = (
        "plant_type",
        "lifecycle",
        "is_published",
    )

    def image_preview(self, obj):
        if obj.primary_image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:4px;" />',
                obj.primary_image.url
            )
        return "—"

    image_preview.short_description = "Image"