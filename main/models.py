from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    value = models.CharField(max_length=255, null=True)
    name = models.TextField()
    color = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.TextField()
    dimension = models.TextField()

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_recipes")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    name = models.TextField()
    image = models.ImageField(upload_to='main/', blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(Product, through='Ingredient', blank=True)
    tag = models.ManyToManyField(Tag, related_name="recipes", blank=True)
    time = models.IntegerField()


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_ingridient")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_ingridient")
    quanity = models.IntegerField()


class ShoppingList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_shoplist")
    recipes = models.ManyToManyField(Recipe, related_name="recipes_shoplist")


class Subscribe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_subscribe")
    followers = models.ManyToManyField(User, related_name="followers_subscribe")


class Favourite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_favourites")
    recipes = models.ManyToManyField(Recipe, related_name="recipes_favourites")
