from django.urls import path

from . import views

urlpatterns = [
    path("",
         views.index_auth,
         name="index"),

    path("new/",
         views.NewRecipe.as_view(),
         name="new_recipe"),

    path("shop/",
         views.shoplist,
         name="shoplist"),

    path("follow/",
         views.follow_view,
         name="follow_view"),

    path("favorite/",
         views.favourite_view,
         name="favourite_view"),

    path("favorites/",
         views.Favorite.as_view(),
         name="add_to_favorite"),

    path("favorites/<int:recipe_id>/",
         views.Favorite.as_view(),
         name="delete_favorite"),

    path("subscriptions/",
         views.Subscribes.as_view(),
         name="add_to_subscribe"),

    path("subscriptions/<int:subscribe_id>/",
         views.Subscribes.as_view(),
         name="delete_subscribe"),

    path("purchases/",
         views.Purchases.as_view(),
         name="add_to_shop"),

    path("purchases/<int:recipe_id>/",
         views.Purchases.as_view(),
         name="shoplist_delete"),

    path("<str:username>/<int:recipe_id>/",
         views.recipe_view,
         name="recipe"),

    path("<str:username>/<int:recipe_id>/edit/",
         views.edit_recipe,
         name="edit_recipe"),

    path("ingredients/",
         views.Ingredients.as_view()),

    path("download/",
         views.download,
         name="download"),

    path("<int:recipe_id>/delete",
         views.recipe_delete,
         name="recipe_delete"),
]
