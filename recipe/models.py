from _ast import mod

from django.conf import settings
from django.db import models
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ingredient Name',
        max_length=64
    )
    description = models.TextField(
        verbose_name='Ingredient Description'
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(
        verbose_name='Recipe Title',
        max_length=200,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Recipe Author',
        on_delete=models.CASCADE,
        default=''
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient used',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe used',
        on_delete=models.CASCADE
    )
    quantity_amount = models.CharField(
        verbose_name='Ingredient quantity',
        max_length=10
    )
    quantity_unit = models.CharField(
        verbose_name='Ingredient quantity units',
        max_length=24
    )