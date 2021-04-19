from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = (
        "pizza_type",
        "pizza_size",
        "count_toppings",
        "toppings",
    )

    list_filter = (
        "pizza_type",
        "pizza_size",
    )

    filter_horizontal = ("pizza_topping",)

    def count_toppings(self, obj):
        return obj.pizza_topping.all().count()

    count_toppings.short_description = "No. of toppings"

    def toppings(self, obj):
        tops = obj.pizza_topping.all()
        strin = ", ".join(top.topping_name for top in tops)
        return strin

    toppings.short_description = "Toppings"


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "size_name",
        "size_diameter",
        "count_pizzas",
    )

    def count_pizzas(self, obj):
        return obj.pizzas.all().count()

    count_pizzas.short_description = "Pizza Count"


@admin.register(models.Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        "topping_name",
        "count_pizzas",
    )

    def count_pizzas(self, obj):
        return obj.pizzas.all().count()

    count_pizzas.short_description = "Pizza Count"
