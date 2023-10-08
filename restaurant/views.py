from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from restaurant.forms import (
    CookCreationForm,
    CookUpdateForm,
    CookSearchForm,
    IngredientSearchForm,
    DishForm,
    DishSearchForm,
    CombinedForm,
)
from restaurant.models import Cook, Dish, Ingredient


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_cookers = Cook.objects.count()
    num_dishes = Dish.objects.count()
    average_experience = Cook.objects.aggregate(
        avg_experience=Avg('years_of_experience'))['avg_experience'] or 0
    total_price = sum(dish.price for dish in Dish.objects.all())
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_cookers": num_cookers,
        "num_dishes": num_dishes,
        "average_experience": int(average_experience),
        "average_price": int(
            total_price / num_dishes if num_dishes > 0 else 0
        ),
        "num_visits": num_visits + 1,
    }
    return render(
        request,
        "restaurant/index.html",
        context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all()
    context_object_name = 'cooker'


class CookBasedView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    success_url = reverse_lazy("restaurant:cook-list")

    def form_valid(self, form):
        driver = form.save(commit=False)
        uploaded_image = self.request.FILES.get("image")
        if uploaded_image:
            if isinstance(uploaded_image, InMemoryUploadedFile):
                driver.image = uploaded_image
        driver.save()
        return super().form_valid(form)


class CookCreateView(CookBasedView):
    form_class = CookCreationForm


class CookUpdateView(CookBasedView, generic.UpdateView):
    form_class = CookUpdateForm


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("restaurant:cook-list")
    context_object_name = 'cooker'


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "restaurant/ingredient_list.html"
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("restaurant:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("restaurant:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("restaurant:ingredient-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("model", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.all().prefetch_related("ingredients")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("restaurant:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("restaurant:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant:dish-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cooker = Cook.objects.get(id=request.user.id)
    if (
        Dish.objects.get(id=pk) in cooker.dishes.all()
    ):
        cooker.dishes.remove(pk)
    else:
        cooker.dishes.add(pk)
    return HttpResponseRedirect(
        reverse_lazy("restaurant:dish-detail", args=[pk])
    )


def register(request):
    if request.method == "POST":
        combined_form = CombinedForm(request.POST)
        if combined_form.is_valid():
            new_user = combined_form.save(commit=False)
            new_user.set_password(combined_form.cleaned_data["password"])
            new_user.save()
            return render(
                request,
                "registration/register_done.html",
                {"new_user": new_user}
            )
    else:
        combined_form = CombinedForm()
    return render(
        request,
        "registration/register.html",
        {"combined_form": combined_form}
    )
