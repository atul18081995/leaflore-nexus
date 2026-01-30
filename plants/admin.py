from django.contrib import admin
from .models import (
    Plant,
    PlantImage,
    PlantCareProfile,
    ClimateCareOverride,
)
from nursery.models import NurseryProfile


# --------------------------------------------------
# Inline: Plant Images
# --------------------------------------------------
class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1
    fields = ("image", "caption", "is_primary", "order")
    ordering = ("order",)


# --------------------------------------------------
# Inline: Nursery Profile (NEW)
# --------------------------------------------------
class NurseryProfileInline(admin.StackedInline):
    model = NurseryProfile
    extra = 0
    max_num = 1
    can_delete = True


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

    # ✅ BOTH image + nursery inline
    inlines = [
        PlantImageInline,
        NurseryProfileInline,
    ]

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

        # ✅ ADD THIS METHOD AT THE BOTTOM OF PlantAdmin
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        from nursery.models import NurseryProfile

        NurseryProfile.objects.get_or_create(
            plant=obj,
            defaults={
                "propagation_method": "Seed",
                "difficulty": "medium",
            }
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

