from rest_framework import serializers

from .models import Product


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "dimension",)
