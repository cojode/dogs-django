from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Breed(models.Model):
    class RatingField(models.IntegerField):
        """Integer in [1;5] range"""

        def __init__(self, *args, **kwargs):
            kwargs.setdefault(
                "validators", [MinValueValidator(1), MaxValueValidator(5)]
            )
            kwargs.setdefault("help_text", "Rating from 1 (low) to 5 (high)")
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            """Deconstruct method."""
            name, path, args, kwargs = super().deconstruct()
            del kwargs["validators"]
            return name, path, args, kwargs

    SIZE_CHOICES = [
        ("Tiny", "Tiny"),
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
    ]

    name = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    friendliness = RatingField()
    trainability = RatingField()
    shedding_amount = RatingField()
    exercise_needs = RatingField()

    def __str__(self):
        return f"{self.name}"


class Dog(models.Model):
    """Dog model linked to a breed."""

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, related_name="dogs"
    )
    gender = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    favorite_food = models.CharField(max_length=100)
    favorite_toy = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.breed})"
