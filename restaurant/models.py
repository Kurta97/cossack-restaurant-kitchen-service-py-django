from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=63, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=50)
        ]
    )
    image = models.ImageField(upload_to="images", blank=True)

    class Meta:
        verbose_name = "cooker"
        verbose_name_plural = "cookers"

    def __str__(self):
        return self.username


class Dish(models.Model):
    name = models.CharField(max_length=127, unique=True)
    description = models.TextField(
        verbose_name="Description", blank=True, null=True
    )
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        Ingredient, related_name='dishes_include'
    )
    cookers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="dishes"
    )
    image = models.ImageField(upload_to="images", blank=True)

    @property
    def price(self):
        total_price = self.ingredients.aggregate(
            Sum("price"))["price__sum"] or 0
        return total_price * 3

    def __str__(self):
        return self.name
