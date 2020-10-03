from django.shortcuts import render, get_object_or_404, redirect
import json
from django.core.paginator import Paginator
from .services import get_ingredients, generate_shop_list
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .models import Tag, Product, Recipe, Ingredient, User, ShoppingList, Subscribe, Favourite
from .forms import RecipeForm
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import IngridientSerializer
from .filters import ProductFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = IngridientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class Ingredients(View):
    def get(self, request):
        text = request.GET['query']
        ingredients = list(Product.objects.filter(
            title__contains=text).values('title', 'dimension'))

        return JsonResponse(ingredients, safe=False)


@login_required()
def favourite_view(request):
    tags_values = request.GET.getlist('filters')
    favorite = Favourite.objects.get(author=request.user)
    recipe_list = favorite.recipes.all()

    if tags_values:
        recipe_list = recipe_list.filter(
            tag__value__in=tags_values).order_by('-pub_date').distinct()

    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        count = ShoppingList.objects.get(author=request.user).recipes.count()
    return render(request, "favorite.html", {"page": page, "paginator": paginator, "count": count})


def indexAuth(request):
    tags = Tag.objects.all()
    tags_values = request.GET.getlist('filters')
    recipe_list = Recipe.objects.all()

    if tags_values:
        recipe_list = recipe_list.filter(
            tag__value__in=tags_values).order_by("-pub_date").distinct().all()

    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'indexAuth.html', {"page": page, "paginator": paginator, "all_tags": tags})


class NewRecipe(View):
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
            for i in range(len(ingredients)):
                if Product.objects.filter(title=ingredients[i][0]).count() == 0:
                    Product.objects.create(title=ingredients[i][0],
                                           dimension=ingredients[i][2])
                ingredient = Ingredient(recipe=new_recipe,
                                        product=Product.objects.get(title=ingredients[i][0]),
                                        quanity=ingredients[i][1])
                ingredient.save()
            tags = ["breakfast", "lunch", "dinner"]
            for i in range(len(tags)):
                if request.POST.get(tags[i]) is not None:
                    new_recipe.tag.add(Tag.objects.get(name=tags[i]))
            return redirect("recipe", username=request.user.username, recipe_id=new_recipe.id)
        else:
            print(form.errors)
        return render(request, "indexAuth.html")


def edit_recipe(request, username, recipe_id):
    count = ShoppingList.objects.get(author=request.user).recipes.count()
    if username == request.user.get_username():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
        if request.method == "POST":
            recipe.recipe_ingridient.all().delete()
            if form.is_valid():
                form.save()
                ingredients = get_ingredients(request)
                for i in range(len(ingredients)):
                    if Product.objects.filter(title=ingredients[i][0]).count() == 0:
                        Product.objects.create(title=ingredients[i][0],
                                               dimension=ingredients[i][2])
                    ingredient = Ingredient(recipe=recipe,
                                            product=Product.objects.get(title=ingredients[i][0]),
                                            quanity=ingredients[i][1])
                    ingredient.save()
                tags = ["breakfast", "lunch", "dinner"]
                for i in range(len(tags)):
                    if request.POST.get(tags[i]) is not None:
                        recipe.tag.add(Tag.objects.get(name=tags[i]))

                return redirect("recipe", username=username, recipe_id=recipe_id)
        return render(request, "formRecipe.html", {"form": form, "count": count})
    return render(request, "indexAuth.html")


@login_required()
def shoplist(request):
    shopping_list = ShoppingList.objects.get(author=request.user)
    return render(request, "shopList.html", {"shopping_list": shopping_list})


@login_required()
def follow_view(request):
    followers = Subscribe.objects.get(author=request.user)
    return render(request, "myFollow.html", {"subs": followers})


class Purchases(View):
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingList.objects.filter(author=request.user).exists():
            shop = ShoppingList.objects.get(author=request.user)
            shop.recipes.add(recipe)
        else:
            shop = ShoppingList(author=request.user)
            shop.recipes.add(recipe)
            shop.save()
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        shop = ShoppingList.objects.get(author=request.user)
        shop.recipes.remove(recipe)
        return JsonResponse({'success': True})


class Favorite(View):
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favourite.objects.filter(author=request.user).exists():
            fav_list = Favourite.objects.get(author=request.user)
            fav_list.recipes.add(recipe)
        else:
            fav_list = Favourite(author=request.user)
            fav_list.recipes.add(recipe)
            fav_list.save()
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        fav_list = Favourite.objects.get(author=request.user)
        fav_list.recipes.remove(recipe)
        return JsonResponse({'success': True})


class Subscribes(View):
    def post(self, request):
        subscribe_id = json.loads(request.body)['id']
        subscriber = get_object_or_404(User, id=subscribe_id)
        if Subscribe.objects.filter(author=request.user).exists():
            subscribe = Subscribe.objects.get(author=request.user)
            subscribe.followers.add(subscriber)
        else:
            subscribe = Subscribe(author=request.user)
            subscribe.save()
            subscribe.followers.add(subscriber)
        return JsonResponse({'success': True})

    def delete(self, request, subscribe_id):
        subscriber = get_object_or_404(User, pk=subscribe_id)
        subscribe = Subscribe.objects.get(author=request.user)
        subscribe.followers.remove(subscriber)
        return JsonResponse({'success': True})


def recipe_view(request, username, recipe_id):
    user = User.objects.get(username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, "singlePage.html", {"recipe": recipe, "tmp_user": user})


@login_required()
def download(request):
    result = generate_shop_list(request)
    filename = 'ingredients.txt'
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
