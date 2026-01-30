from django.urls import path
from django.http import HttpResponse
from .views import add_to_wishlist

from nursery import views

# Temporary placeholder view
def nursery_home(request):
    return HttpResponse("Nursery module active")

urlpatterns = [
    path("", nursery_home, name="nursery-home"),
        path(
        "notify/<int:plant_id>/",
        views.notify_when_available,
        name="nursery-notify",
    ),
    path("wishlist/add/<int:plant_id>/", add_to_wishlist, name="wishlist-add")
]