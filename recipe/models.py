from _ast import mod

from django.conf import settings
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")

    created_time = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class RecipeIngredients(models.Model):
    pass


class Ingredient(models.Model):

    pass