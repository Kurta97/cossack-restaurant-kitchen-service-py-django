from django.contrib.auth import get_user_model
from django.test import TestCase

from restaurant.models import Dish, DishType, Ingredient


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.cooker = get_user_model().objects.create_user(
            username="rambo1982",
            years_of_experience=10,
            password="test1234",
            first_name="John",
            last_name="Rambo",
        )
        self.dish_type = DishType.objects.create(name="main_course")
        self.ingredient = Ingredient.objects.create(name="cheese", price=5)
        self.dish = Dish.objects.create(
            name="pizza",
            description="the_best_pizza_ever",
            dish_type=self.dish_type,
        )
        self.dish.ingredients.set([self.ingredient, ])
        self.dish.cookers.set([self.cooker, ])

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)

    def test_ingredient_price(self):
        self.assertEqual(self.ingredient.price, 5)

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_cooker_str(self):
        self.assertEqual(str(self.cooker), self.cooker.username)

    def test_cooker_years_of_experience(self):
        self.assertEqual(self.cooker.years_of_experience, 10)

    def test_dish_str(self):
        self.assertEqual(str(self.dish), self.dish.name)

    def test_dish_description(self):
        self.assertEqual(self.dish.description, "the_best_pizza_ever")

    def test_dish_dish_type(self):
        self.assertEqual(str(self.dish.dish_type), "main_course")

    def test_dish_ingredients(self):
        queryset = self.dish.ingredients.values_list()
        self.assertEqual(queryset[0][1], "cheese")

    def test_dish_cookers(self):
        cookers = self.dish.cookers.all()
        cooker = []
        for cook in cookers:
            cooker.append(cook.username)
        self.assertEqual(cooker, ["rambo1982"])

    def test_dish_price(self):
        self.assertEqual(self.dish.price, 15)
