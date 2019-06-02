from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredients


# Register your models here.
class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    can_delete = False


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # list_display = ('title', 'author', 'ingredients')
    ordering = ('title', 'author')
    search_fields = ('title', 'author', 'ingredients')
    inlines = (RecipeIngredientInline,)

admin.site.register(Ingredient)

