from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Public website
    path("plants/", include("plants.urls")),

    # API
    path("api/", include("plants.api_urls")),

    # Nursery module
    path("nursery/", include("nursery.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )