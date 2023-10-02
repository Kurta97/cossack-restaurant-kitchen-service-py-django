from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from restaurant.forms import (
    CookCreationForm,
    CookUpdateForm,
    CookSearchForm,
)
from restaurant.models import Cook, Dish


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
    paginate_by = 5

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


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    context_object_name = 'cooker'
    success_url = reverse_lazy("restaurant:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("restaurant:cook-list")
    context_object_name = 'cooker'


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("restaurant:cook-list")
    context_object_name = 'cooker'
