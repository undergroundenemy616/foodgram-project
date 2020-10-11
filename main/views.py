import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django_filters import rest_framework as filters
from rest_framework import viewsets

from .filters import ProductFilter
from .forms import RecipeForm
from .models import (Favourite, Ingredient, Product, Recipe, ShoppingList,
                     Subscribe, Tag, User)
from .serializers import IngridientSerializer
from .services import generate_shop_list, get_ingredients
from django.contrib.auth.mixins import LoginRequiredMixin


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = IngridientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class Ingredients(View):
    def get(self, request):
        text = request.GET["query"]
        ingredients = list(Product.objects.filter(
            title__contains=text).values("title", "dimension"))

        return JsonResponse(ingredients, safe=False)


@login_required()
def favourite_view(request):
    tags_values = request.GET.getlist("filters")
    favorite, flag = Favourite.objects.get_or_create(author=request.user)
    recipe_list = favorite.recipes.all()

    if tags_values:
        recipe_list = recipe_list.filter(
            tag__value__in=tags_values).order_by("-pub_date").distinct()

    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "favorite.html", {"page": page,
                                             "paginator": paginator,})


def index_auth(request):
    tags = Tag.objects.all()
    tags_values = request.GET.getlist("filters")
    recipe_list = Recipe.objects.all()

    if tags_values:
        recipe_list = recipe_list.filter(
            tag__value__in=tags_values).order_by("-pub_date").distinct().all()

    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "indexAuth.html", {"page": page,
                                              "paginator": paginator,
                                              "all_tags": tags})


class NewRecipe(LoginRequiredMixin, View):
    def get(self, request):
        form = RecipeForm()
        return render(request, "formRecipe.html", {"form": form})

    def post(self, request):
        form = RecipeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            ingredients = get_ingredients(request)
            for ingr in ingredients:
                Product.objects.get_or_create(title=ingr[0],
                                              dimension=ingr[2])
                product = get_object_or_404(Product, title=ingr[0])
                ingredient = Ingredient(recipe=new_recipe,
                                        product=product,
                                        quanity=ingr[1])
                ingredient.save()
            tags = ["breakfast", "lunch", "dinner"]
            for tag in tags:
                if request.POST.get(tag) is not None:
                    current_tag = get_object_or_404(Tag, name=tag)
                    new_recipe.tag.add(current_tag)
            return redirect("recipe",
                            username=request.user.username,
                            recipe_id=new_recipe.id)
        return render(request, "indexAuth.html")


@login_required()
def edit_recipe(request, username, recipe_id):
    if username != request.user.get_username():
        return render(request, "indexAuth.html")

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)

    if request.method != "POST":
        return render(request, "formChangeRecipe.html", {"form": form,
                                                         "recipe_id": recipe_id,
                                                         "username": username})
    recipe.ingredients.all().delete()
    if form.is_valid():
        form.save()
        ingredients = get_ingredients(request)
        for ingr in ingredients:
            Product.objects.get_or_create(title=ingr[0],
                                          dimension=ingr[2])

            product = get_object_or_404(Product, title=ingr[0])
            ingredient = Ingredient(recipe=recipe,
                                    product=product,
                                    quanity=ingr[1])

            ingredient.save()
        tags = ["breakfast", "lunch", "dinner"]
        for tag in tags:
            if request.POST.get(tag[1]) is not None:
                current_tag = get_object_or_404(Tag, name=tag)
                recipe.tag.add(current_tag)

        return redirect("recipe",
                        username=username,
                        recipe_id=recipe_id)

    return render(request, "formChangeRecipe.html", {"form": form,
                                                     "recipe_id": recipe_id,
                                                     "username": username})


@login_required()
def shoplist(request):
    shopping_list, flag = ShoppingList.objects.get_or_create(author=request.user)
    return render(request, "shopList.html", {"shopping_list": shopping_list})


@login_required()
def follow_view(request):
    followers, flag = Subscribe.objects.get_or_create(author=request.user)
    return render(request, "myFollow.html", {"subs": followers})


class Purchases(View):
    def post(self, request):
        recipe_id = json.loads(request.body)["id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shop, created = ShoppingList.objects.get_or_create(author=request.user)
        shop.recipes.add(recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        shop = get_object_or_404(ShoppingList, author=request.user)
        shop.recipes.remove(recipe)
        return JsonResponse({"success": True})


class Favorite(View):
    def post(self, request):
        recipe_id = json.loads(request.body)["id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        fav_list, created = Favourite.objects.get_or_create(author=request.user)
        fav_list.recipes.add(recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        fav_list = get_object_or_404(Favourite, author=request.user)
        fav_list.recipes.remove(recipe)
        return JsonResponse({"success": True})


class Subscribes(View):
    def post(self, request):
        subscribe_id = json.loads(request.body)["id"]
        subscriber = get_object_or_404(User, id=subscribe_id)
        subscribe, created = Subscribe.objects.get_or_create(author=request.user)
        subscribe.followers.add(subscriber)
        return JsonResponse({"success": True})

    def delete(self, request, subscribe_id):
        subscriber = get_object_or_404(User, pk=subscribe_id)
        subscribe = get_object_or_404(Subscribe, author=request.user)
        subscribe.followers.remove(subscriber)
        return JsonResponse({"success": True})


def recipe_view(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, "singlePage.html", {"recipe": recipe,
                                               "tmp_user": user})


@login_required()
def download(request):
    result = generate_shop_list(request)
    filename = "ingredients.txt"
    response = HttpResponse(result, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    return response


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect("index")


def page_not_found(request, exception):
    return render(request,
                  "404.html",
                  {"path": request.path},
                  status=404)


def server_error(request):
    return render(request, "500.html", status=500)
