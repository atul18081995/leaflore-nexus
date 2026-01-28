from django.urls import path
from .views import PlantListAPIView

urlpatterns = [
    path("plants/", PlantListAPIView.as_view(), name="plant-list"),
]