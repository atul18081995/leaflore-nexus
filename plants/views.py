from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import Plant
from .serializers import PlantSerializer


# --------------------
# API views
# --------------------

class PlantListAPIView(ListAPIView):
    queryset = Plant.objects.filter(is_published=True)
    serializer_class = PlantSerializer


# --------------------
# Web views (public)
# --------------------

from django.db.models import Q

def plant_list_view(request):
    query = request.GET.get("q", "").strip()

    plants = Plant.objects.filter(is_published=True)

    if query:
        plants = plants.filter(
            Q(common_name__icontains=query)
            | Q(scientific_name__icontains=query)
            | Q(family__icontains=query)
            | Q(genus__icontains=query)
        )

    return render(
        request,
        "plants/plant_list.html",
        {
            "plants": plants,
            "query": query,
        },
    )

def plant_detail_view(request, slug):
    plant = get_object_or_404(
        Plant,
        slug=slug,
        is_published=True,
    )

    # ✅ Primary image logic (SAFE for templates)
    primary_image = (
        plant.images.filter(is_primary=True).first()
        or plant.images.first()
    )

    return render(
        request,
        "plants/plant_detail.html",
        {
            "plant": plant,
            "primary_image": primary_image,
        },
    )