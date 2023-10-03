from django.urls import path

from restaurant import views
from restaurant.views import (
    CookDetailView,
    CookDeleteView,
    CookListView,
    CookCreateView,
    CookUpdateView,
    IngredientListView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    toggle_assign_to_dish,
)

app_name = "restaurant"

urlpatterns = [
    path("", views.index, name="index"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path(
        "cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
    path("cook/create/", CookCreateView.as_view(), name="cook-create"),
    path(
        "cook/<int:pk>/update/",
        CookUpdateView.as_view(),
        name="cook-update",
    ),
    path(
        "cook/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete",
    ),
    path(
        "ingredient/",
        IngredientListView.as_view(),
        name="ingredient-list",
    ),
    path(
        "ingredient/create/",
        IngredientCreateView.as_view(),
        name="ingredient-create",
    ),
    path(
        "ingredient/<int:pk>/update/",
        IngredientUpdateView.as_view(),
        name="ingredient-update",
    ),
    path(
        "ingredient/<int:pk>/delete/",
        IngredientDeleteView.as_view(),
        name="ingredient-delete",
    ),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path(
        "dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"
    ),
    path(
        "dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"
    ),
    path(
        "dish/<int:pk>/toggle-assign/",
        toggle_assign_to_dish,
        name="toggle-dish-assign",
    ),
]
