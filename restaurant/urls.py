from django.urls import path

from restaurant import views
from restaurant.views import (
    CookDetailView,
    CookDeleteView,
    CookListView,
    CookCreateView,
    CookUpdateView,
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
]
