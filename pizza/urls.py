from django.urls import path
from . import views

app_name = "pizza"
urlpatterns = [
    path("pizza/", views.all_pizzas, name="all_pizzas"),
    path("pizza/createSquare", views.create_square_pizza, name="create_square_pizza"),
    path(
        "pizza/createRegular", views.create_regular_pizza, name="create_regular_pizza"
    ),
    path("pizza/<int:pizza_id>", views.one_pizza, name="one_pizza"),
]
