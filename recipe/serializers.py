from rest_framework import serializers

from .models import *
from user.models import UserProfile, UserAccount


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(
                **{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'tag_text',)


class IngredientDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')


# class AuthorSerializer(serializers.ModelSerializer):
#     user_account = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=UserAccount.objects.all()
#     )

#     class Meta:
#         model = UserProfile
#         fields = ('user_account',)


class RecipeTagSerializer(serializers.ModelSerializer):
    tag = CustomSlugRelatedField(
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = CustomSlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all()
    )

    quantity_amount = serializers.CharField()
    quantity_unit = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity_amount', 'quantity_unit')
        # fields = '__all__'


class RecipeStepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    step_number = serializers.IntegerField()

    class Meta:
        model = RecipeStep
        fields = ('id', 'step_number', 'step_text')


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
    # author = serializers.StringRelatedField()

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

    def create(self, validated_data):
        author = validated_data.pop('author')
        author_profile = UserProfile.objects.get(id=author.id)
        tags_data = validated_data.pop('recipe_tags')
        ingredients_data = validated_data.pop('recipe_ingredients')
        steps_data = validated_data.pop('steps')
        notes_data = validated_data.pop('notes')

        recipe = Recipe(**validated_data)
        recipe.author = author_profile
        recipe.save()
        for tag in tags_data:
            tag, created = Tag.objects.get_or_create(tag_text=tag['tag'])
            recipe_tag = RecipeTag.objects.create(tag=tag, recipe=recipe)

        for ing in ingredients_data:
            ingObj, created = Ingredient.objects.get_or_create(
                name=ing['ingredient'])
            recipe_ingredient = RecipeIngredient.objects.create(
                ingredient=ingObj,
                recipe=recipe,
                quantity_amount=ing['quantity_amount'],
                quantity_unit=ing['quantity_unit'])

        for step in steps_data:
            recipe_step = RecipeStep.objects.create(
                recipe=recipe,
                step_number=step['step_number'],
                step_text=step['step_text']
            )

        for note in notes_data:
            recipe_note = RecipeNote.objects.create(
                recipe=recipe,
                note_text=note['note_text']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.author = validated_data['author']
        instance.save()

        # Remove tags that were deleted
        new_tags = [tag['tag'] for tag in validated_data['recipe_tags']]
        for tag in instance.recipe_tags.all():
            if tag.tag not in new_tags:
                tag.delete()

        # Create or update tags
        for tag in validated_data['recipe_tags']:
            tagObj, created = Tag.objects.get_or_create(
                tag_text=tag['tag']
            )
            print(tagObj, created)

            recipe_tag, created = RecipeTag.objects.get_or_create(
                tag=tagObj, recipe=instance)
            # recipe_tag.save()

        # Remove ingredients that were deleted
        new_ingredients = [ing['ingredient']
                           for ing in validated_data['recipe_ingredients']]
        for ing in instance.recipe_ingredients.all():
            if ing.ingredient not in new_ingredients:
                print('DELETING', ing)
                ing.delete()

        # Create or update ingredients
        for ing in validated_data['recipe_ingredients']:
            ingObj, created = Ingredient.objects.get_or_create(
                name=ing['ingredient']
            )
            # try:
            #     ingObj = Ingredient.objects.get(name=ing['ingredient'])
            # except Ingredient.DoesNotExist:
            #     ingObj = Ingredient(name=ing['ingredient'], description='')
            #     ingObj.save()

            recipe_ingredient, created = RecipeIngredient.objects.update_or_create(
                ingredient=ing['ingredient'],
                recipe=instance,
                defaults={
                    'quantity_amount': ing['quantity_amount'],
                    'quantity_unit': ing['quantity_unit']
                }
            )

        # Steps
        new_step_nums = [step['step_number']
                         for step in validated_data['steps']]
        for step in instance.steps.all():
            if step.step_number not in new_step_nums:
                print('DELETING', step)
                step.delete()
                # Something to decrement all steps after?

        for step in validated_data['steps']:
            recipe_step, created = RecipeStep.objects.update_or_create(
                step_number=step['step_number'],
                recipe=instance,
                defaults={
                    'step_text': step['step_text'],
                }
            )

        # Notes
        new_notes = [note['note_text'] for note in validated_data['notes']]
        for note in instance.notes.all():
            if note.note_text not in new_notes:
                print('DELETING', note)
                note.delete()

        for note in validated_data['notes']:
            recipe_note, created = RecipeNote.objects.get_or_create(
                note_text=note['note_text'],
                recipe=instance
            )

        return instance
