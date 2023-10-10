from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, PasswordInput

from .models import Dish, Cook, DishType, Ingredient


class CookCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
            "image",
        )


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = [
            "years_of_experience",
            "first_name",
            "last_name",
            "email",
            "image"
        ]


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class DishForm(forms.ModelForm):
    cookers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all(),
        widget=forms.Select,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class CombinedForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ("username", "first_name", "last_name", "email", "password")
        widgets = {
            "username": TextInput(attrs={
                "placeholder": "Please enter your username"
            }),
            "first_name": TextInput(attrs={
                "placeholder": "Please enter your first name (optional)"
            }),
            "last_name": TextInput(attrs={
                "placeholder": "Please enter your last name (optional)"
            }),
            "email": EmailInput(attrs={
                "placeholder": "Please enter your email (optional)"
            }),
            "password": PasswordInput(attrs={
                "placeholder": "Please enter your password"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None
