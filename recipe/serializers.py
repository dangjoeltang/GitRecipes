from rest_framework import serializers

from .models import *

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('tag_text',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'description')
    

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()
    quantity_amount = serializers.StringRelatedField()
    quantity_unit = serializers.StringRelatedField()
    
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity_amount', 'quantity_unit')


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ('step_number', 'step_text')


class RecipeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNote
        fields = ('note_text',)


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    # recipe_ingredients = serializers.StringRelatedField(many=True)
    ingredients = RecipeIngredientSerializer(source='recipe_ingredients', many=True)
    steps = RecipeStepSerializer(many=True)
    tags = TagSerializer(many=True)
    notes = RecipeNoteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('title', 'author', 'ingredients', 'tags', 'steps', 'notes', 'created_time', 'modified_time')
