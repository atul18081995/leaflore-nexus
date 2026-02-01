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

    # ----------------------------------
    # Primary image
    # ----------------------------------
    primary_image = (
        plant.images.filter(is_primary=True).first()
        or plant.images.first()
    )

    # ----------------------------------
    # Nursery (safe)
    # ----------------------------------
    nursery = getattr(plant, "nursery", None)

    # ----------------------------------
    # Get alternatives (exclude self)
    # ----------------------------------
    alternative_engine = PlantAlternativeEngine(plant)
    raw_alternatives = [
        alt for alt in alternative_engine.get_alternatives(limit=12)
        if alt.id != plant.id
    ]

    if not raw_alternatives:
        raw_alternatives = (
            Plant.objects
            .filter(is_published=True)
            .exclude(id=plant.id)
            .order_by("?")[:6]
        )

    # ----------------------------------
    # 1️⃣ Nursery recommendations
    # ONLY sellable plants
    # ----------------------------------
    nursery_recommendations = []
    nursery_ids = set()

# 1️⃣ Prefer sellable alternatives
    for alt in raw_alternatives:
        alt_nursery = getattr(alt, "nursery", None)
        if alt_nursery and alt_nursery.is_sellable:
            nursery_recommendations.append(alt)

    # 2️⃣ Fallback: coming soon alternatives
    if not nursery_recommendations:
        for alt in raw_alternatives:
            alt_nursery = getattr(alt, "nursery", None)
            if alt_nursery and not alt_nursery.is_sellable:
                nursery_recommendations.append(alt)

# 3️⃣ Final fallback: knowledge-only
    if not nursery_recommendations:
        for alt in raw_alternatives:
            alt_nursery = getattr(alt, "nursery", None)
            if not alt_nursery:
                nursery_recommendations.append(alt)
    for alt in raw_alternatives:
        alt_nursery = getattr(alt, "nursery", None)
        if alt_nursery and alt_nursery.is_sellable:
            nursery_recommendations.append(alt)
            nursery_ids.add(alt.id)

    nursery_recommendations = nursery_recommendations[:3]

    # ----------------------------------
    # 2️⃣ Bottom recommendations
    # (exclude nursery ones to avoid duplicates)
    # ----------------------------------
    available_recommendations = []
    unavailable_recommendations = []
    knowledge_recommendations = []

    for alt in raw_alternatives:
        if alt.id in nursery_ids:
            continue

        alt_nursery = getattr(alt, "nursery", None)

        if alt_nursery:
            if alt_nursery.is_sellable:
                available_recommendations.append(alt)
            else:
                unavailable_recommendations.append(alt)
        else:
            knowledge_recommendations.append(alt)

    # ----------------------------------
    # Reason text (bottom section)
    # ----------------------------------
    if nursery and not nursery.is_sellable:
        recommendation_reason = (
            "Since this plant is currently unavailable, you can consider these alternatives."
        )
    else:
        recommendation_reason = (
            "You may also be interested in these similar plants."
        )

    # ----------------------------------
    # Context
    # ----------------------------------
    context = {
        "plant": plant,
        "primary_image": primary_image,
        "nursery": nursery,

        # Nursery section
        "nursery_recommendations": nursery_recommendations,

        # Bottom section
        "available_recommendations": available_recommendations[:6],
        "unavailable_recommendations": unavailable_recommendations[:6],
        "knowledge_recommendations": knowledge_recommendations[:6],
        "recommendation_reason": recommendation_reason,
    }

    return render(
        request,
        "plants/plant_detail.html",
        context,
    )