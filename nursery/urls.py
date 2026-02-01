from django.urls import path
from django.http import HttpResponse
from nursery import views

app_name = "nursery"   # ✅ REQUIRED

# Temporary placeholder view
def nursery_home(request):
    return HttpResponse("Nursery module active")

urlpatterns = [
    path("", nursery_home, name="home"),

    path(
        "notify/<int:plant_id>/",
        views.notify_when_available,
        name="notify",           # ✅ underscore
    ),

    path(
        "wishlist/add/<int:plant_id>/",
        views.add_to_wishlist,
        name="wishlist_add",     # ✅ underscore
    ),
]