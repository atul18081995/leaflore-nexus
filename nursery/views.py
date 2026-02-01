from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from plants.models import Plant
from .models import StockNotification, Wishlist


def notify_when_available(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        email = request.POST.get("email")

        StockNotification.objects.get_or_create(
            plant=plant,
            email=email,
        )

        messages.success(
            request,
            "You'll be notified when this plant is available 🌱"
        )

    # ✅ FIXED redirect
    return redirect("plants:plant_detail", slug=plant.slug)


def add_to_wishlist(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.user.is_authenticated:
        Wishlist.objects.get_or_create(
            user=request.user,
            plant=plant
        )
    else:
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Please enter an email to save wishlist.")
            return redirect("plants:plant_detail", slug=plant.slug)

        Wishlist.objects.get_or_create(
            email=email,
            plant=plant
        )

    messages.success(request, "❤️ Added to your wishlist!")

    # (Optional but cleaner than HTTP_REFERER)
    return redirect("plants:plant_detail", slug=plant.slug)