from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from restaurant.models import DishType, Dish, Cook, Ingredient


@admin.register(DishType)
class DishType(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name", "dish_type", "price"]
    list_filter = ["dish_type"]
    search_fields = ["name"]


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", )
    list_filter = ["years_of_experience"]
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info", {"fields": ("years_of_experience",)},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info", {"fields": ("years_of_experience",)},
        ),
    )
    search_fields = ["username"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    search_fields = ["name"]
