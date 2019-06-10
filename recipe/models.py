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

    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name='Ingredient'
        verbose_name_plural='Ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_text = models.CharField(
        verbose_name='Tag',
        max_length=24
    )

    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name='Tag'
        verbose_name_plural='Tags'

    def __str__(self):
        return self.tag_text


class Recipe(models.Model):
    title = models.CharField(
        verbose_name='Recipe Title',
        max_length=200,
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

    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name='Recipe'
        verbose_name_plural='Recipes'

    def __str__(self):
        return self.title


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
        verbose_name='Step in Recipe'
        verbose_name_plural='Steps in Recipe'
        unique_together=('id', 'step_number')

    def __str__(self):
        return str(self.step_number)

    # Deleting a middle step will not decrement all the following steps
    def save(self, force_insert=False, force_update=False):
        if self.step_number == 0:
            try:
                recent = RecipeStep.objects.filter(recipe__exact=self.recipe).order_by('-step_number')[0]
                self.step_number = recent.step_number + 1
            except IndexError:
                self.step_number = 1
        super(RecipeStep, self).save(force_insert, force_update)


class RecipeNote(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note_text = models.TextField(
        verbose_name = 'Note'
    )
    # created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name='Note about Recipe'
        verbose_name_plural='Notes about Recipe'
    
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
        verbose_name='Ingredient used in Recipe'
        verbose_name_plural='Ingredients used in Recipe'
    
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
        verbose_name='Tag in Recipe'
        verbose_name_plural='Tags in Recipe'


