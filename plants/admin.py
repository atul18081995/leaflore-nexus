from django.contrib import admin
from .models import (
    Plant,
    PlantImage,
    PlantCareProfile,
    ClimateCareOverride,
)


# --------------------------------------------------
# Inline: Plant Images
# --------------------------------------------------
class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1
    fields = ("image", "caption", "is_primary", "order")
    ordering = ("order",)


# --------------------------------------------------
# Plant Admin (STRUCTURED VIEW)
# --------------------------------------------------
@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):

    list_display = (
        "common_name",
        "scientific_name",
        "family",
        "plant_type",
        "is_published",
    )

    search_fields = (
        "common_name",
        "scientific_name",
        "family",
        "genus",
    )

    list_filter = (
        "plant_type",
        "lifecycle",
        "family",
        "is_published",
    )

    prepopulated_fields = {"slug": ("scientific_name",)}

    inlines = [PlantImageInline]

    fieldsets = (
        ("Basic Identity", {
            "fields": (
                "common_name",
                "scientific_name",
                "slug",
                "family",
                "genus",
                "species",
                "description",
            )
        }),
        ("Classification", {
            "fields": (
                "plant_type",
                "lifecycle",
                "growth_habit",
            )
        }),
        ("Morphology", {
            "fields": (
                "height",
                "canopy_spread",
                "leaf_description",
                "flower_description",
                "fruit_description",
                "bark_description",
            )
        }),
        ("Origin & Ecology", {
            "fields": (
                "origin_region",
                "native_range",
            )
        }),
        ("Uses", {
            "fields": (
                "medicinal_uses",
                "agricultural_uses",
                "cultural_significance",
            )
        }),
        ("Safety", {
            "fields": (
                "toxicity",
                "precautions",
            )
        }),
        ("Media & Publishing", {
            "fields": (
                "primary_image",
                "is_published",
            )
        }),
    )


# --------------------------------------------------
# Climate Care Inline
# --------------------------------------------------
class ClimateCareInline(admin.TabularInline):
    model = ClimateCareOverride
    extra = 1


# --------------------------------------------------
# Plant Care Profile Admin
# --------------------------------------------------
@admin.register(PlantCareProfile)
class PlantCareProfileAdmin(admin.ModelAdmin):

    list_display = (
        "plant",
        "light_requirement",
        "indoor_outdoor",
    )

    inlines = [ClimateCareInline]