from rest_framework import serializers

from .models import *
from user.models import UserProfile

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('tag_text',)


class AuthorSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UserProfile
        fields = ('id',)


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
        fields = ('pk', 'title', 'author', 'ingredients', 'tags', 'steps', 'notes', 'created_time', 'modified_time')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        steps_data = validated_data.pop('steps')

        print(validated_data)
        author_profile = UserProfile.objects.get(user_account=author)
        recipe = Recipe.objects.create(
            author_id = author_profile.id
            **validated_data
        )
        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(
                ingredient, created = Ingredient.objects.get_or_create(name=ingredient['name'])
                **recipe_ingredient_data
                # quantity_amount = ingredient['quantity_amount']
                # quantity_unit = ingredient['quantity_unit']
                # ingredient, created = Ingredient.objects.get_or_create(name=ingredient_data['name'])
                # quantity_amount = ingredient_data['quantity_amount']
                # quantity_unit = ingredient_data['quantity_unit']
            )
            recipe.ingredients.add(ingredient)
        recipe.save()
        return recipe


class RecipeListSerializer(serializers.HyperlinkedModelSerializer):
    # author = serializers.HyperlinkedRelatedField(
    #     queryset = UserProfile.objects.all(),
    #     view_name = 'profile-detail'
    # )
    author = serializers.PrimaryKeyRelatedField(
        queryset = UserProfile.objects.all()
    )

    num_ingredients = serializers.IntegerField(source='recipe_ingredients.count', read_only=True)
    num_steps = serializers.IntegerField(source='steps.count', read_only=True)
    tags = TagSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Recipe
        fields = ('pk', 'url', 'title', 'author', 'num_ingredients', 'tags', 'num_steps', 'created_time', 'modified_time')
        extra_kwargs = {
            'url': {'view_name': 'recipe-detail'}
        }

    def create(self, validated_data):
        author = validated_data.pop('author')
        author_profile = UserProfile.objects.get(id=author.id)
        tags_data = validated_data.pop('tags')
        recipe = Recipe(**validated_data)
        recipe.author = author_profile
        recipe.save()
        for tag in tags_data:
            tag, created = Tag.objects.get_or_create(tag_text=tag['tag_text'])
            recipe_tag = RecipeTag.objects.create(tag=tag, recipe=recipe)
            # recipe.tags.add(recipe_tag)
            recipe_tag.save()
        # recipe.save()
        return recipe

