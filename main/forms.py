from .models import Recipe
from django.forms import ModelForm
from django import forms


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ("name", "tag", "ingredient", "time", "description", "image")
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8, 'class': 'form__textarea'}),
        }
