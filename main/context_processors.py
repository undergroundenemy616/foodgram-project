from.models import ShoppingList


def counter(request):
    if request.user.is_authenticated:
        shoplist, flag = ShoppingList.objects.get_or_create(author=request.user)
        count = len(shoplist.recipes.all())
    else:
        count = []
    return {'count': count}
