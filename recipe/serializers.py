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


class IngredientDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
    

class RecipeIngredientSerializer(serializers.ModelSerializer):
    # ingredient = IngredientSerializer()
    ingredient = serializers.SlugRelatedField(
        slug_field = 'name',
        queryset = Ingredient.objects.all()
    )

    quantity_amount = serializers.CharField()
    quantity_unit = serializers.CharField()
    
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
 
    def update(self, instance, validated_data):
        recipe_ingredients_data = validated_data.pop('recipe_ingredients')
        
        recipe_ingredients = instance.recipe_ingredients

        # Check for updates with a recipe ingredient's quantity for this recipe
        for recipe_ingredient_data in recipe_ingredients_data:
            recipe_ingredient, created = RecipeIngredient.objects.update_or_create(
                ingredient = recipe_ingredient_data.get('ingredient', None),
                recipe = instance,
                defaults = {
                    'quantity_amount': recipe_ingredient_data.get('quantity_amount', None),
                    'quantity_unit': recipe_ingredient_data.get('quantity_unit')
                }
            )
            recipe_ingredient.save()

        return instance


class RecipeListSerializer(serializers.HyperlinkedModelSerializer):
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


class RecipeIngredientSetSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        # view_name='recipe-detail',
        # read_only=True
        queryset = Recipe.objects.all()
    )

    ingredient = IngredientSerializer()
    # ingredient = serializers.SlugRelatedField(
    #     slug_field = 'name',
    #     queryset = Ingredient.objects.all()
    # )

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        print(ingredient_data)
        ingredient, created = Ingredient.objects.get_or_create(
            name = ingredient_data.get('name'),
            defaults = {'description': 'No description provided'}
        )
        recipe_ingredient = RecipeIngredient(**validated_data)
        recipe_ingredient.ingredient = ingredient
        recipe_ingredient.save()
        return recipe_ingredient

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
