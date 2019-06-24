from rest_framework import serializers

from .models import *
from user.models import UserProfile


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'tag_text',)


class RecipeTagSerializer(serializers.ModelSerializer):
    # tag = TagSerializer()
    tag = serializers.SlugRelatedField(
        slug_field='tag_text',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = RecipeTag
        fields = ('tag',)

    def create(self, validated_data):
        tag_data = validated_data.pop('tag')
        tag, created = Tag.objects.get_or_create(
            tag_text=tag_data.get('tag_text')
        )
        recipe_tag = RecipeTag(**validated_data)
        recipe_tag.tag = tag
        recipe_tag.save()
        return recipe_tag

    # def update(self, instance, validated_data):


class IngredientDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all()
    )

    quantity_amount = serializers.CharField()
    quantity_unit = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity_amount', 'quantity_unit')
        # fields = '__all__'

    # def create(self, validated_data):
    #     ingredient_data = validated_data.pop('ingredient')
    #     ingredient, created = Ingredient.objects.get_or_create(

    #     )


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ('step_number', 'step_text')


class RecipeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNote
        fields = ('note_text',)


class RecipeListSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all()
    )

    num_ingredients = serializers.IntegerField(
        source='recipe_ingredients.count', read_only=True)
    num_steps = serializers.IntegerField(source='steps.count', read_only=True)
    tags = TagSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Recipe
        fields = ('pk', 'url', 'title', 'author', 'num_ingredients',
                  'tags', 'num_steps', 'created_time', 'modified_time')
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
            recipe_tag.save()
        return recipe


class RecipeIngredientSetSerializer(serializers.ModelSerializer):
    # recipe = serializers.PrimaryKeyRelatedField(
    #     queryset = Recipe.objects.all()
    # )

    ingredient = IngredientSerializer()

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        ingredient, created = Ingredient.objects.get_or_create(
            name=ingredient_data.get('name'),
            defaults={'description': 'No description provided'}
        )
        recipe_ingredient = RecipeIngredient(**validated_data)
        recipe_ingredient.ingredient = ingredient
        recipe_ingredient.save()
        return recipe_ingredient

    def update(self, instance, validated_data):
        # No need to change ingredient model. Just delete and add new ingredient
        # PUT for recipe_ingredient is jsut for updating quantity details
        instance.quantity_amount = validated_data.get(
            'quantity_amount', instance.quantity_amount)
        instance.quantity_unit = validated_data.get(
            'quantity_unit', instance.quantity_unit)
        instance.save()
        return instance

    class Meta:
        model = RecipeIngredient
        # fields = '__all__'
        exclude = ('recipe',)


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    ingredients = RecipeIngredientSetSerializer(
        source='recipe_ingredients', many=True)
    steps = RecipeStepSerializer(source='recipe_steps', many=True)
    tags = TagSerializer(source='recipe_tags', many=True)
    notes = RecipeNoteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('pk', 'title', 'author', 'ingredients', 'tags',
                  'steps', 'notes', 'created_time', 'modified_time')

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.save()

        # Update Ingredients
        recipe_ingredients_data = validated_data.pop('recipe_ingredients')

        recipe_ingredients = instance.recipe_ingredients

        # Check for updates with a recipe ingredient's quantity for this recipe
        for recipe_ingredient_data in recipe_ingredients_data:
            recipe_ingredient, created = RecipeIngredient.objects.update_or_create(
                ingredient=recipe_ingredient_data.get('ingredient', None),
                recipe=instance,
                defaults={
                    'quantity_amount': recipe_ingredient_data.get('quantity_amount', None),
                    'quantity_unit': recipe_ingredient_data.get('quantity_unit')
                }
            )
            recipe_ingredient.save()

        # Update Tags
        # Delete removed tags
        # tag_ids = [tag.get('id') for tag in validated_data['tags']]
        # print(tag_ids)
        # for tag in instance.tags:
        #     if tag.id not in tag_ids:
        #         tag.delete()

        # for tag in validated_data['tags']:
        #     tag, created = Tag.objects.get_or_create(tag_text = tag['tag_text'])
        #     recipe_tag = RecipeTag.objects.create(tag=tag, recipe=instance)

        return instance


class GenericRecipeSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=UserProfile.objects.all()
    # )

    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True
    )

    tags = RecipeTagSerializer(
        source='recipe_tags',
        many=True
    )

    steps = RecipeStepSerializer(
        # source='recipe_steps',
        many=True
    )

    notes = RecipeNoteSerializer(
        many=True
    )

    class Meta:
        model = Recipe
        # fields = '__all__'
        fields = ('pk', 'title', 'author', 'ingredients', 'tags',
                  'steps', 'notes', 'created_time', 'modified_time')

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.author = validated_data['author']
        instance.save()
        print('update')

        # Remove tags that were deleted
        new_tags = [tag['tag'] for tag in validated_data['recipe_tags']]
        for tag in instance.recipe_tags.all():
            if tag not in new_tags:
                tag.delete()

        # Create or update tags
        for tag in validated_data['recipe_tags']:
            tagObj, created = Tag.objects.get_or_create(
                tag_text=tag['tag']
            )

            recipe_tag = RecipeTag.objects.create(tag=tagObj, recipe=instance)
            print(recipe_tag)
            recipe_tag.save()

        # # Remove ingredients that were deleted
        # new_ingredients = [ing['ingredient']
        #                    for ing in validated_data['recipe_ingredients']]
        # print(new_ingredients)
        # for ing in instance.recipe_ingredients.all():
        #     if ing not in new_ingredients:
        #         ing.delete()

        # # Create or update ingredients
        # for ing in validated_data['recipe_ingredients']:
        #     print(ing)
        #     # ingObj, created = Ingredient.objects.get_or_create(
        #     #     name=ing['ingredient']
        #     # )
        #     try:
        #         ingObj = Ingredient.objects.get(name=ing['ingredient'])
        #     except Ingredient.DoesNotExist:
        #         ingObj = Ingredient(name=ing['ingredient'], description='')
        #         ingObj.save()

        #     print(ingObj, created)

        #     recipe_ingredient, created = RecipeIngredient.objects.update_or_create(
        #         ingredient=ing['ingredient'],
        #         recipe=instance,
        #         defaults={
        #             'quantity_amount': ing['quantity_amount'],
        #             'quantity_unit': ing['quantity_unit']
        #         }
        #     )
        #     print(recipe_ingredient)
        #     recipe_ingredient.save()

        return instance
