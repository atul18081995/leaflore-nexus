from rest_framework import serializers
from .models import Plant


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            "id",
            "common_name",
            "scientific_name",
            "family",
            "genus",
            "description",
            "medicinal_uses",
            "growth_conditions",
        ]