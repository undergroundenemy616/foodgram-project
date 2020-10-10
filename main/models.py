from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    value = models.CharField(max_length=255,
                             verbose_name="Значение тега",
                             null=True)
    name = models.TextField(verbose_name="Название тега")
    color = models.TextField(verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.TextField(verbose_name="Название продукта")
    dimension = models.TextField(verbose_name="Единицы измерения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name="Автор рецепта")
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True,)
    name = models.TextField(verbose_name="Название рецепта")
    image = models.ImageField(upload_to="main/",
                              verbose_name="Изображение продукта",
                              blank=True,
                              null=True,)
    description = models.TextField(verbose_name="Описание продукта")
    ingredient = models.ManyToManyField(Product, through='Ingredient', blank=True)
    tag = models.ManyToManyField(Tag, related_name="recipes", blank=True)
    time = models.IntegerField(verbose_name="Время приготовления")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ('pub_date',)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="ingredients")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="ingredients")
    quanity = models.IntegerField(verbose_name="Количество ингредиента")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class ShoppingList(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="shoplist")
    recipes = models.ManyToManyField(Recipe,
                                     related_name="shoplist",
                                     verbose_name="Количество ингредиента")

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"


class Subscribe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,)
    followers = models.ManyToManyField(User,
                                       related_name="subscribes")

    verbose_name = "Подписчики автора"

    class Meta:
        verbose_name_plural = "Подписчики авторов"


class Favourite(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="favourites")
    recipes = models.ManyToManyField(Recipe,
                                     related_name="favourites")

    class Meta:
        verbose_name = "Избранное автора"
        verbose_name_plural = "Избранное авторов"
