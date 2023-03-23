from django.urls import path, include
from rest_framework.routers import DefaultRouter

from breaking_bad.views import CharacterViewSet, LocationViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"character", CharacterViewSet, basename="character")
router.register(r"location", LocationViewSet, basename="location")

urlpatterns = [
    path("", include(router.urls))
]
