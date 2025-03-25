from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BreedViewSet, DogViewSet

router = DefaultRouter()
router.register(r"breeds", BreedViewSet)
router.register(r"dogs", DogViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
