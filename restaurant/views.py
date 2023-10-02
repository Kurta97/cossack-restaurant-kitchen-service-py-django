from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
