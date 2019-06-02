from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient


# Register your models here.
class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 1
    can_delete = False


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # list_display = ('title', 'author', 'ingredients')
    ordering = ('title', 'author')
    search_fields = ('title', 'author', 'ingredients')
    list_display = ('title', 'author', 'modified_time', 'created_time', )
    inlines = (RecipeIngredientInline,)


admin.site.register(Ingredient)

