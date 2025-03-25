from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Breed, Dog


class DogAPITests(APITestCase):
    def setUp(self):
        self.breed1 = Breed.objects.create(
            name="Labrador",
            size="Large",
            friendliness=5,
            trainability=5,
            shedding_amount=3,
            exercise_needs=4,
        )
        self.breed2 = Breed.objects.create(
            name="Poodle",
            size="Medium",
            friendliness=4,
            trainability=5,
            shedding_amount=2,
            exercise_needs=3,
        )

        self.dog1 = Dog.objects.create(
            name="Max",
            age=3,
            breed=self.breed1,
            gender="Male",
            color="Yellow",
            favorite_food="Kibble",
            favorite_toy="Ball",
        )
        self.dog2 = Dog.objects.create(
            name="Bella",
            age=5,
            breed=self.breed1,
            gender="Female",
            color="Black",
            favorite_food="Chicken",
            favorite_toy="Frisbee",
        )
        self.dog3 = Dog.objects.create(
            name="Charlie",
            age=2,
            breed=self.breed2,
            gender="Male",
            color="White",
            favorite_food="Fish",
            favorite_toy="Rope",
        )

    def test_breed_list(self):
        url = reverse("breed-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        labrador_data = next(
            b for b in response.data if b["name"] == "Labrador"
        )
        self.assertEqual(labrador_data["dog_count"], 2)
        poodle_data = next(b for b in response.data if b["name"] == "Poodle")
        self.assertEqual(poodle_data["dog_count"], 1)

    def test_dog_list(self):
        url = reverse("dog-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        max_data = next(d for d in response.data if d["name"] == "Max")
        self.assertEqual(max_data["average_age"], 4.0)
        charlie_data = next(d for d in response.data if d["name"] == "Charlie")
        self.assertEqual(charlie_data["average_age"], 2.0)

    def test_dog_detail(self):
        url = reverse("dog-detail", args=[self.dog1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Max")
        self.assertEqual(response.data["breed_count"], 2)

    def test_create_dog(self):
        url = reverse("dog-list")
        data = {
            "name": "Luna",
            "age": 4,
            "breed_id": self.breed1.id,
            "gender": "Female",
            "color": "Brown",
            "favorite_food": "Beef",
            "favorite_toy": "Bone",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.count(), 4)
        self.assertEqual(Dog.objects.get(name="Luna").breed.name, "Labrador")

    def test_update_dog(self):
        url = reverse("dog-detail", args=[self.dog1.id])
        data = {
            "name": "Maximus",
            "age": 4,
            "breed_id": self.breed1.id,
            "gender": "Male",
            "color": "Yellow",
            "favorite_food": "Kibble",
            "favorite_toy": "Ball",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.get(id=self.dog1.id).name, "Maximus")

    def test_partial_update_dog(self):
        url = reverse("dog-detail", args=[self.dog1.id])
        data = {"name": "Maximilian"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.get(id=self.dog1.id).name, "Maximilian")

    def test_delete_dog(self):
        url = reverse("dog-detail", args=[self.dog1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.count(), 2)

    def test_breed_rating_validation(self):
        url = reverse("breed-list")
        data = {
            "name": "Invalid",
            "size": "Large",
            "friendliness": 6,
            "trainability": 5,
            "shedding_amount": 3,
            "exercise_needs": 4,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("friendliness", response.data)

    def test_dog_age_validation(self):
        url = reverse("dog-list")
        data = {
            "name": "Puppy",
            "age": -1,
            "breed_id": self.breed1.id,
            "gender": "Male",
            "color": "Brown",
            "favorite_food": "Milk",
            "favorite_toy": "Chew Toy",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", response.data)

    def test_breed_with_no_dogs(self):
        Breed.objects.create(
            name="Shiba",
            size="Medium",
            friendliness=3,
            trainability=3,
            shedding_amount=3,
            exercise_needs=3,
        )
        url = reverse("breed-list")
        response = self.client.get(url)
        shiba_data = next(b for b in response.data if b["name"] == "Shiba")
        self.assertEqual(shiba_data["dog_count"], 0)

    def test_dog_without_breed(self):
        url = reverse("dog-list")
        data = {
            "name": "NoBreed",
            "age": 1,
            "breed_id": 999,
            "gender": "Male",
            "color": "Black",
            "favorite_food": "Anything",
            "favorite_toy": "Everything",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_breed_unique_name(self):
        url = reverse("breed-list")
        data = {
            "name": "Labrador",
            "size": "Large",
            "friendliness": 5,
            "trainability": 5,
            "shedding_amount": 3,
            "exercise_needs": 4,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
