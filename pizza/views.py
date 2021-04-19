from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from . import models
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers

# Create your views here.


@api_view(
    [
        "GET",
    ]
)
def all_pizzas(request):
    print("request query params= ", request.query_params)
    print("request= ", request.method)
    pizzatype = request.query_params.get("type")
    print("pizza type= ", pizzatype)
    pizzasize = request.query_params.get("size")
    print("pizza size= ", pizzasize)
    queryset = models.Pizza.objects.all()
    if pizzatype is not None:
        print("filter pizzas by type= ", pizzatype)
        queryset = queryset.filter(pizza_type__iexact=str(pizzatype).strip())
    if pizzasize is not None:
        print("filter pizzas by size= ", pizzasize)
        queryset = queryset.filter(pizza_size__size_name__iexact=str(pizzasize).strip())
    data = serializers.PizzaSerializer(queryset, many=True).data
    print("data= ", data)
    # content = JSONRenderer().render(data)
    # return JsonResponse(data, status=200, safe=False)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def one_pizza(request, pizza_id):
    print("request= ", request)
    print("request= ", request.method)
    print("request data= ", request.data)
    print("pizza id= ", pizza_id)
    try:
        pizza = models.Pizza.objects.get(id=pizza_id)
        print("pizza= ", pizza)
    except models.Pizza.DoesNotExist:
        return JsonResponse({"error": "Pizza Not Found"}, status=404, safe=False)

    if request.method == "GET":
        return JsonResponse(
            serializers.PizzaSerializer(instance=pizza).data,
            status=200,
            safe=False,
        )
    elif request.method == "DELETE":
        pizza.delete()
        return Response({"success": "Pizza Deleted"}, status=status.HTTP_202_ACCEPTED)
    elif request.method == "PUT":

        type = request.data.get("type")
        print("type=", type)
        if type is not None:
            type = str(type).lower().strip()
            print("updating pizza type to ", type)
            if type not in [models.Pizza.PIZZA_SQUARE, models.Pizza.PIZZA_REGULAR]:
                return Response(
                    {"error": "Invalid Pizza Type"}, status=status.HTTP_404_NOT_FOUND
                )
            else:
                pizza.pizza_type = type

        size = request.data.get("size")
        print("size= ", size)
        if size is not None:
            try:
                psize = models.Size.objects.get(
                    size_name__iexact=str(size).capitalize().strip()
                )
                print("updating pizza size to, ", psize)
            except models.Size.DoesNotExist:
                return Response(
                    {"error": "Invalid Pizza Size"}, status=status.HTTP_404_NOT_FOUND
                )
            pizza.pizza_size = psize

        toppings = request.data.get("topping")
        print("toppings= ", toppings)

        if toppings is not None:
            ptoppings = []
            for topping in toppings:
                try:
                    ptop = models.Topping.objects.get(topping_name__iexact=topping)
                    print("adding topping ", ptop)
                    ptoppings.append(ptop.id)
                except models.Topping.DoesNotExist:
                    return Response(
                        {"error": "Invalid Pizza Topping"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            pizza.pizza_topping.set(ptoppings)
        pizza.save()
        data = serializers.PizzaSerializer(instance=pizza).data
        return Response(data, status=status.HTTP_202_ACCEPTED)
    return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def create_square_pizza(request):
    print("request= ", request.method)
    print(request.data)
    size = request.data.get("size")
    print("size= ", size)
    toppings = request.data.get("topping")
    print("toppings= ", toppings)

    if size is None:
        return JsonResponse("Size is required", status=412, safe="False")
    if toppings is None:
        return JsonResponse("One Topping is required", status=412, safe="False")

    size = str(size).capitalize()
    print("capitalized size= ", size)
    try:
        psize = models.Size.objects.get(size_name=size)
        print("pizza size= ", psize)
    except models.Size.DoesNotExist:
        return JsonResponse("Invalid Size", status=404, safe=False)

    ptoppings_ids = []
    for t in toppings:
        print(t)
        try:
            top = models.Topping.objects.get(topping_name=str(t).capitalize().strip())
            print(top)
        except models.Topping.DoesNotExist:
            return JsonResponse("Invalid Topping", status=404, safe=False)
        ptoppings_ids.append(top.id)

    print(ptoppings_ids)
    try:
        newpizza = models.Pizza.objects.create(
            pizza_type=models.Pizza.PIZZA_SQUARE,
            pizza_size=psize,
        )
        newpizza.save()
        newpizza.pizza_topping.set(ptoppings_ids)
    except Exception:
        return Response(status=status.status.HTTP_500_INTERNAL_SERVER_ERROR)
    print("new pizza= ", newpizza)
    print("new pizza= ", newpizza.id)
    data = serializers.PizzaSerializer(instance=newpizza).data
    return Response(data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
def create_regular_pizza(request):
    print("request= ", request.method)
    print(request.data)
    size = request.data.get("size")
    print("size= ", size)
    toppings = request.data.get("topping")
    print("toppings= ", toppings)

    if size is None:
        return JsonResponse({"error": "Size is required"}, status=412, safe=False)
    if toppings is None:
        return JsonResponse(
            {"error": "One Topping is required"}, status=412, safe=False
        )

    size = str(size).capitalize()
    print("capitalized size= ", size)
    try:
        psize = models.Size.objects.get(size_name=size)
        print("pizza size= ", psize)
    except models.Size.DoesNotExist:
        return JsonResponse({"error": "Invalid Size"}, status=404, safe=False)

    ptoppings_ids = []
    for t in toppings:
        print(t)
        try:
            top = models.Topping.objects.get(topping_name=str(t).capitalize().strip())
            print(top)
        except models.Topping.DoesNotExist:
            return JsonResponse({"error": "Invalid Topping"}, status=404, safe=False)
        ptoppings_ids.append(top.id)

    print(ptoppings_ids)
    try:
        newpizza = models.Pizza.objects.create(
            pizza_type=models.Pizza.PIZZA_REGULAR,
            pizza_size=psize,
        )
        newpizza.save()
        newpizza.pizza_topping.set(ptoppings_ids)
    except Exception:
        return Response(status=status.status.HTTP_500_INTERNAL_SERVER_ERROR)
    print("new pizza= ", newpizza)
    print("new pizza= ", newpizza.id)
    data = serializers.PizzaSerializer(instance=newpizza).data
    return Response(data, status=status.HTTP_201_CREATED)
