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
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def get_queryset(self):
        if self.action == "list":
            return Breed.objects.annotate(dog_count=Count("dogs"))
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return BreedListSerializer
        return super().get_serializer_class()
