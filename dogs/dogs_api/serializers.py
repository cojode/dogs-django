from rest_framework import serializers

from .models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = [
            "id",
            "name",
            "size",
            "friendliness",
            "trainability",
            "shedding_amount",
            "exercise_needs",
        ]
        extra_kwargs = {
            "friendliness": {"min_value": 1, "max_value": 5},
            "trainability": {"min_value": 1, "max_value": 5},
            "shedding_amount": {"min_value": 1, "max_value": 5},
            "exercise_needs": {"min_value": 1, "max_value": 5},
        }


class DogSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    breed_id = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), source="breed", write_only=True
    )

    class Meta:
        model = Dog
        fields = [
            "id",
            "name",
            "age",
            "breed",
            "breed_id",
            "gender",
            "color",
            "favorite_food",
            "favorite_toy",
        ]
