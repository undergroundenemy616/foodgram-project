from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    query = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["title"]
