from .models import ShoppingList
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def get_ingredients(request):
    ingredients_list = []
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value = key[15:]
            ingredient = []
            ingredient.append(request.POST.get("nameIngredient_" + value))
            ingredient.append(request.POST.get("valueIngredient_" + value))
            ingredient.append(request.POST.get("unitsIngredient_" + value))
            ingredients_list.append(ingredient)
    return ingredients_list


def generate_shop_list(request):
    shop_list = get_object_or_404(ShoppingList, author=request.user)
    ingredients_dict = {}

    for recipe in shop_list.recipes.all():
        for ingredient in recipe.recipe_ingridient.all():
            name = f'{ingredient.product.title} ({ingredient.product.dimension})'
            if name in ingredients_dict.keys():
                ingredients_dict[name] += ingredient.quanity
            else:
                ingredients_dict[name] = ingredient.quanity

    ingredients_list = []
    for key, value in ingredients_dict.items():
        ingredients_list.append(f'{key} - {value},')

    return ingredients_list


