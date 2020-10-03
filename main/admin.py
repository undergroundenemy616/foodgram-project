from django.contrib import admin
from .models import *


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('pk', 'name', 'author', 'pub_date', 'description',
                    'image', 'time')
    search_fields = ("name",)
    list_filter = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ("title",)
    list_filter = ('title',)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingList)
admin.site.register(Subscribe)
admin.site.register(Favourite)
