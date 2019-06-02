from django.contrib import admin

from .models import Ingredient, Tag, Recipe, RecipeIngredient, RecipeTag, RecipeStep


# Register your models here.
class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    can_delete = False


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0
    can_delete = False

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 0
    can_delete = True
    exclude=['step_number']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # list_display = ('title', 'author', 'ingredients')
    ordering = ('title', 'author')
    search_fields = ('title', 'author', 'ingredients')
    list_display = ('title', 'author', 'modified_time', 'created_time', )
    inlines = (RecipeIngredientInline, RecipeTagInline, RecipeStepInline)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    list_display = ('name', 'modified_time', 'created_time', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ('tag_text',)
    search_fields = ('tag_text',)
