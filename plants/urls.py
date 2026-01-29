from django.urls import path
from .views import plant_list_view, plant_detail_view

urlpatterns = [
    path("", plant_list_view, name="plant-list"),
    path("<slug:slug>/", plant_detail_view, name="plant-detail"),
]