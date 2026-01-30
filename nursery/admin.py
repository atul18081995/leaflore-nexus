from django.contrib import admin
from .models import NurseryProfile


@admin.register(NurseryProfile)
class NurseryProfileAdmin(admin.ModelAdmin):
    list_display = (
        "plant",
        "is_sellable",
        "difficulty",
        "propagation_method",
    )
    list_filter = ("is_sellable", "difficulty")
    search_fields = (
        "plant__common_name",
        "plant__scientific_name",
    )