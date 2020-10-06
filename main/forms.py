from django import forms
from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ("name", "tag", "ingredient", "time", "description", "image")
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8, 'class': 'form__textarea'}),
        }
