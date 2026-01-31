from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.generics import ListAPIView

from .models import Plant
from .serializers import PlantSerializer
from services.alternative_engine import PlantAlternativeEngine


# --------------------------------------------------
# API VIEWS
# --------------------------------------------------

class PlantListAPIView(ListAPIView):
    queryset = Plant.objects.filter(is_published=True)
    serializer_class = PlantSerializer


# --------------------------------------------------
# WEB VIEWS (PUBLIC)
# --------------------------------------------------

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

    context = {
        "plants": plants,
        "query": query,
    }

    return render(
        request,
        "plants/plant_list.html",
        context,
    )


def plant_detail_view(request, slug):
    plant = get_object_or_404(
        Plant,
        slug=slug,
        is_published=True,
    )

    # --------------------------------------------------
    # PRIMARY IMAGE (SAFE – NO TEMPLATE LOGIC BREAK)
    # --------------------------------------------------
    primary_image = (
        plant.images.filter(is_primary=True).first()
        or plant.images.first()
    )

    # --------------------------------------------------
    # AI ALTERNATIVE ENGINE
    # --------------------------------------------------
    alternative_engine = PlantAlternativeEngine(plant)
    alternatives = alternative_engine.get_alternatives(limit=4)

    # --------------------------------------------------
    # TEMPLATE CONTEXT (SINGLE SOURCE OF TRUTH)
    # --------------------------------------------------
    context = {
        "plant": plant,
        "primary_image": primary_image,
        "alternatives": alternatives,

        # Used to highlight AI alternatives when plant
        # is not sellable in nursery
        "show_alternative_highlight": not (
            plant.has_nursery and plant.nursery.is_sellable
        ),
    }

    return render(
        request,
        "plants/plant_detail.html",
        context,
    )