from django.db import models

# Create your models here.


class Size(models.Model):
    size_name = models.CharField(max_length=40)
    size_diameter = models.IntegerField()

    def __str__(self) -> str:
        return self.size_name + " " + str(self.size_diameter)


class Topping(models.Model):
    topping_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.topping_name


class Pizza(models.Model):

    PIZZA_REGULAR = "regular"
    PIZZA_SQUARE = "square"
    PIZZA_TYPES = (
        (PIZZA_REGULAR, "Regular"),
        (PIZZA_SQUARE, "Square"),
    )

    pizza_type = models.CharField(
        max_length=20, choices=PIZZA_TYPES, default=PIZZA_REGULAR
    )
    pizza_size = models.ForeignKey(
        Size,
        related_name="pizzas",
        related_query_name="size",
        on_delete=models.CASCADE,
    )
    pizza_topping = models.ManyToManyField(
        Topping,
        related_name="pizzas",
    )

    def __str__(self) -> str:
        return self.pizza_size.size_name + "-" + self.pizza_type
