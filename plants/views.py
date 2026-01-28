from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Plant
from .serializers import PlantSerializer


class PlantListAPIView(ListAPIView):
    queryset = Plant.objects.filter(is_published=True)
    serializer_class = PlantSerializer

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = [
        "common_name",
        "scientific_name",
        "family",
        "genus",
        "medicinal_uses",
    ]

    ordering_fields = [
        "common_name",
        "scientific_name",
        "family",
        "created_at",
    ]

    ordering = ["common_name"]