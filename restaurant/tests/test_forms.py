from django.contrib.auth import get_user_model
from django.test import TestCase
from restaurant.forms import (
    CookCreationForm,
    CookUpdateForm,
    CookSearchForm,
    IngredientSearchForm,
    DishForm,
    DishSearchForm,
    CombinedForm)

from restaurant.models import DishType, Ingredient


class FormTests(TestCase):
    def test_cook_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_creation_form_invalid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "wrongpassword",  # Invalid password confirmation
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cook_update_form_valid(self):
        form_data = {
            "years_of_experience": 10,
            "image": "example.jpg",
        }
        form = CookUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_search_form_valid(self):
        form_data = {
            "username": "testuser",
        }
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ingredient_search_form_valid(self):
        form_data = {
            "name": "Test Ingredient",
        }
        form = IngredientSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_form_valid(self):
        self.cooker = get_user_model().objects.create_user(
            username="test_rambo1982",
            years_of_experience=10,
            password="test1234",
            first_name="John",
            last_name="Rambo",
        )
        self.dish_type = DishType.objects.create(name="test_course")
        self.ingredient = Ingredient.objects.create(name="test", price=5)
        data = {
            'name': 'Test Dish',
            "dish_type": self.dish_type.id,
            "ingredients": [self.ingredient.id],
            "cookers": [self.cooker.id]
        }
        form = DishForm(data)
        self.assertTrue(form.is_valid())

    def test_dish_form_invalid(self):
        form_data = {
            "name": "Test Dish",
            "cookers": [],  # Invalid: No Cooks selected
            "dish_type": None,  # Invalid: No DishType selected
            "ingredients": [1, 2],
            # Replace with valid Ingredient IDs from your database
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_dish_search_form_valid(self):
        form_data = {
            "name": "Test Dish",
        }
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_combined_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password": "testpassword123",
        }
        form = CombinedForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_combined_form_invalid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "wrongpassword",
        }
        form = CombinedForm(data=form_data)
        self.assertFalse(form.is_valid())
