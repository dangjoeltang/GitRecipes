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
            self.fail('invalid, custom slug field error')


# class AuthorSerializer(serializers.ModelSerializer):
#     user_account = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=UserAccount.objects.all()
#     )

#     class Meta:
#         model = UserProfile
#         fields = ('user_account',)


class IngredientDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag_text',)


class RecipeTagSerializer(serializers.ModelSerializer):
    tag = CustomSlugRelatedField(
        slug_field='tag_text',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = RecipeTag
        fields = ('tag',)

    def to_representation(self, instance):
        tagObj = super().to_representation(instance)
        return tagObj['tag']

    def to_internal_value(self, data):
        return {'tag': data}

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
    step_number = serializers.IntegerField()

    class Meta:
        model = RecipeStep
        fields = ('step_number', 'step_text')


class RecipeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNote
        fields = ('note_text',)


class RecipePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipePhoto
        fields = ('photo_text', 'photo_file')


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

    recipe_photos = RecipePhotoSerializer(
        many=True,
        # required=False
    )

    class Meta:
        model = Recipe
        # fields = '__all__'
        fields = ('pk', 'title', 'author', 'privacy', 'description', 'ingredients', 'tags',
                  #   'steps', 'notes', 'created_time', 'modified_time')
                  'steps', 'notes', 'recipe_photos', 'created_time', 'modified_time')

    def create(self, validated_data):
        print(validated_data)
        author = validated_data.pop('author')
        author_profile = UserProfile.objects.get(id=author.id)
        tags_data = validated_data.pop('recipe_tags')
        ingredients_data = validated_data.pop('recipe_ingredients')
        steps_data = validated_data.pop('steps')
        notes_data = validated_data.pop('notes')
        photos_data = validated_data.pop('recipe_photos')

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
        for photo in photos_data:
            recipe_photo = RecipePhoto.objects.create(
                recipe=recipe,
                photo_text=photo['photo_text'],
                photo_file=photo['photo_file']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.author = validated_data['author']
        instance.privacy = validated_data['privacy']
        instance.photos = validated_data['recipe_photos']
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
