from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from restaurant.models import Cook, Dish, DishType, Ingredient

HOME_URL = reverse("restaurant:index")
COOKER_URL = reverse("restaurant:cook-list")
DISH_URL = reverse("restaurant:dish-list")
INGREDIENT_URL = reverse("restaurant:ingredient-list")


class TestViewsLoginRequired(TestCase):
    def test_login_required_home(self):
        response = self.client.get(HOME_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cooker_list(self):
        response = self.client.get(COOKER_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_list(self):
        response = self.client.get(DISH_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_ingredient_list(self):
        response = self.client.get(INGREDIENT_URL)
        self.assertNotEquals(response.status_code, 200)


class TestViewsPagesForRegisteredUser(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="rambo1982",
            password="JustWantToEatButHaveToKill82",
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(name="test", price=5)
        self.dish_type = DishType.objects.create(name="main_course")
        self.dish = Dish.objects.create(
            name="pizza",
            description="the_best_pizza_ever",
            dish_type=self.dish_type,
        )
        self.dish.ingredients.set([self.ingredient])
        self.dish.cookers.set([self.user])

    def test_retrieve_ingredient_list(self):
        Ingredient.objects.create(name="test2", price=5)
        Ingredient.objects.create(name="test3", price=5)
        Ingredient.objects.create(name="test4", price=5)

        response = self.client.get(INGREDIENT_URL)
        self.assertEquals(response.status_code, 200)

        ingredients = Ingredient.objects.all()
        self.assertEquals(
            list(response.context["ingredient_list"]),
            list(ingredients)
        )

        self.assertTemplateUsed(
            response,
            "restaurant/ingredient_list.html"
        )

    def test_retrieve_dish_list(self):
        response = self.client.get(DISH_URL)
        self.assertEquals(response.status_code, 200)

        ingredients = Dish.objects.all()
        self.assertEquals(
            list(response.context["dish_list"]),
            list(ingredients)
        )

        self.assertTemplateUsed(
            response,
            "restaurant/dish_list.html"
        )

    def test_retrieve_cooker_list(self):
        response = self.client.get(COOKER_URL)
        self.assertEquals(response.status_code, 200)

        ingredients = Cook.objects.all()
        self.assertEquals(
            list(response.context["cook_list"]),
            list(ingredients)
        )

        self.assertTemplateUsed(
            response,
            "restaurant/cook_list.html"
        )
