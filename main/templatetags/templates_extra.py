from django import template
from ..models import ShoppingList, Subscribe, Favourite

register = template.Library()


@register.filter(name='is_shop')
def is_shop(recipe, user):
    try:
        shop = ShoppingList.objects.get(author=user)
        if recipe in shop.recipes.all():
            return True
        else:
            return False
    except ShoppingList.DoesNotExist:
        return False


@register.filter(name='is_follow')
def is_follow(follower, user):
    try:
        subscribe = Subscribe.objects.get(author=user)
        if follower in subscribe.followers.all():
            return True
        else:
            return False
    except Subscribe.DoesNotExist:
        return False


@register.filter(name='is_favorite')
def is_favorite(favorite, user):
    try:
        favorites = Favourite.objects.get(author=user)
        if favorite in favorites.recipes.all():
            return True
        else:
            return False
    except Favourite.DoesNotExist:
        return False


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    if tag.value in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.value)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.value)

    return new_request.urlencode()
