from django.db.models import Avg, Count
from rest_framework import viewsets

from .models import Breed, Dog
from .serializers import (
    BreedListSerializer,
    BreedSerializer,
    DogDetailSerializer,
    DogListSerializer,
    DogSerializer,
)


class DogViewSet(viewsets.ModelViewSet):
    """Dog model viewset, featuring two extended overriden actions."""
    
    """
    # * GET [list] /api/dogs/
    # ? also includes information about average age of a dog with the same breed.
    #
    # * POST /api/dogs/
    #
    # * GET /api/dogs/<id>
    # ? also includes dog count with the same breed (breed_count).
    #
    # * PUT /api/dogs/<id>
    #
    # * DELETE /api/dogs/<id>
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_serializer_class(self):
        serializer_options = {
            "list": DogListSerializer,
            "retrieve": DogDetailSerializer,
        }
        return serializer_options.get(
            self.action, super().get_serializer_class()
        )

    def get_queryset(self):
        match self.action:
            case "list":
                return Dog.objects.annotate(
                    average_age=Avg("breed__dogs__age")
                ).select_related("breed")
            case "retrieve":
                return Dog.objects.annotate(
                    breed_count=Count("breed__dogs")
                ).select_related("breed")
        return super().get_queryset()


class BreedViewSet(viewsets.ModelViewSet):
    """Breed model viewset, featuring one extended overriden action."""
    
    """
    # * GET [list] /api/breeds/
    # ? also includes information about average age of a dog with the same breed.
    #
    # * POST /api/breeds/
    #
    # * GET /api/breeds/<id>
    #
    # * PUT /api/breeds/<id>
    #
    # * DELETE /api/breeds/<id>
    """
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def get_queryset(self):
        match self.action:
            case "list":
                return Breed.objects.annotate(dog_count=Count("dogs"))
        return super().get_queryset()

    def get_serializer_class(self):
        serializer_options = {"list": BreedListSerializer}
        return serializer_options.get(
            self.action, super().get_serializer_class()
        )
