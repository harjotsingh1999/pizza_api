from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from . import models


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topping
        fields = ("topping_name",)


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = ("size_name",)


class PizzaSerializer(serializers.ModelSerializer):
    pizza_topping = SlugRelatedField(
        read_only=True, many=True, slug_field="topping_name"
    )
    pizza_size = SlugRelatedField(read_only=True, slug_field="size_name")

    class Meta:
        model = models.Pizza
        fields = (
            "id",
            "pizza_type",
            "pizza_size",
            "pizza_topping",
        )
