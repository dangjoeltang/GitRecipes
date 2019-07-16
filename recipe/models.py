from _ast import mod

from django.conf import settings
from django.db import models
from django.utils import timezone

from user.models import UserProfile


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ingredient Name',
        max_length=64
    )
    description = models.TextField(
        verbose_name='Ingredient Description',
        blank=True
    )

    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_text = models.CharField(
        verbose_name='Tag',
        max_length=24
    )

    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag_text


class Recipe(models.Model):
    title = models.CharField(
        verbose_name='Recipe Title',
        max_length=200,
    )

    privacy = models.CharField(
        max_length=10,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('secret', 'Secret')
        ],
        default='public'
    )

    description = models.CharField(
        verbose_name='Recipe Description',
        max_length=400,
        blank=True,
        default='No description available.'
    )

    author = models.ForeignKey(
        UserProfile,
        verbose_name='Recipe Author',
        related_name='author_recipes',
        on_delete=models.CASCADE,
        default=''
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag'
    )

    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title


class RecipePhotos(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_photos'
    )
    photo_text = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )
    photo_file = models.FileField(
        upload_to='recipes/',
        blank=True
    )

    uploaded_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.id


class RecipeStep(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    step_number = models.PositiveSmallIntegerField(
        default=0
    )
    step_text = models.TextField(
        verbose_name='Step Directions'
    )

    class Meta:
        verbose_name = 'Step in Recipe'
        verbose_name_plural = 'Steps in Recipe'

    def __str__(self):
        return str(self.step_number)


class RecipeNote(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note_text = models.TextField(
        verbose_name='Note'
    )
    # created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Note about Recipe'
        verbose_name_plural = 'Notes about Recipe'

    def __str__(self):
        return self.note_text


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient used',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe used',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    quantity_amount = models.CharField(
        verbose_name='Ingredient quantity',
        max_length=10
    )
    quantity_unit = models.CharField(
        verbose_name='Ingredient quantity units',
        max_length=24,
        blank=True
    )

    class Meta:
        verbose_name = 'Ingredient used in Recipe'
        verbose_name_plural = 'Ingredients used in Recipe'

    def __str__(self):
        return '{0} - {1} {2}'.format(self.ingredient, self.quantity_amount, self.quantity_unit)


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        verbose_name='Tag used',
        on_delete=models.CASCADE,

    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe tagged',
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )

    class Meta:
        verbose_name = 'Tag in Recipe'
        verbose_name_plural = 'Tags in Recipe'
