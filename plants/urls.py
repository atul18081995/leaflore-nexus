from django.urls import path
from . import views

app_name = "plants"   # <-- KEEP THIS

urlpatterns = [
    path(
        "",
        views.plant_list_view,
        name="plant_list",
    ),
    path(
        "<slug:slug>/",
        views.plant_detail_view,
        name="plant_detail",
    ),
]