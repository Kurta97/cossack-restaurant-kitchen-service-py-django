from django.urls import path

from restaurant import views

app_name = "restaurant"

urlpatterns = [
    path("", views.index, name="index"),
]
