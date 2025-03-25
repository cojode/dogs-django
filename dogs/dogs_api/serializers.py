from rest_framework import serializers

from .models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    """Base Breed serializer class."""
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
    """Base Dog serializer class."""
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
        extra_kwargs = {"age": {"min_value": 0}}


class DogListSerializer(DogSerializer):
    """Specific Dog list serializer, featuring average_age field."""
    average_age = serializers.FloatField(read_only=True)

    class Meta(DogSerializer.Meta):
        fields = DogSerializer.Meta.fields + ["average_age"]


class DogDetailSerializer(DogSerializer):
    """Specific Dog detail serializer, featuring breed_count field."""
    breed_count = serializers.IntegerField(read_only=True)

    class Meta(DogSerializer.Meta):
        fields = DogSerializer.Meta.fields + ["breed_count"]


class BreedListSerializer(BreedSerializer):
    """Specific Breed list serializer, featuring dog_count field."""
    dog_count = serializers.IntegerField(read_only=True)

    class Meta(BreedSerializer.Meta):
        fields = BreedSerializer.Meta.fields + ["dog_count"]
