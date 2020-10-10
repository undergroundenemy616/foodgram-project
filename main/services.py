from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import ShoppingList

User = get_user_model()


def get_ingredients(request):
    ingredients = []
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value = key[15:]
            ingredient = []
            ingredient.append(request.POST.get("nameIngredient_" + value))
            ingredient.append(request.POST.get("valueIngredient_" + value))
            ingredient.append(request.POST.get("unitsIngredient_" + value))
            ingredients.append(ingredient)
    return ingredients


def generate_shop_list(request):
    shop_list = get_object_or_404(ShoppingList, author=request.user)
    ingredients = {}

    for recipe in shop_list.recipes.all():
        for ingredient in recipe.recipe_ingridient.all():
            name = f'{ingredient.product.title} ({ingredient.product.dimension})'
            if name in ingredients:
                ingredients[name] += ingredient.quanity
            else:
                ingredients[name] = ingredient.quanity

    ingredients_list = []
    for key, value in ingredients.items():
        ingredients_list.append(f'{key} - {value},')

    return ingredients_list
