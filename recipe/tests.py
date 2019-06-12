from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from .models import *
from user.models import UserAccount, UserProfile


class BaseModelsTest(APITestCase):

    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email = 'recipetest@unittest.com',
            username = 'recipeunittest',
            first_name = 'recipe',
            last_name = 'test',
            password = 'password'
        )
        self.profile = UserProfile.objects.create(
            user_account = self.user
        )
        self.tag = Tag.objects.create(
            tag_text = 'Tag test text'
        )
        self.ingredient = Ingredient.objects.create(
            name = 'Test Ingredient',
            description = 'Test description of test ingredient'
        )
        self.recipe = Recipe.objects.create(
            title = 'Test Recipe Title',
            author = self.profile
        )
        self.recipe_step = RecipeStep.objects.create(
            recipe = self.recipe,
            step_number = 1,
            step_text = 'This is the first step'
        )
        self.recipe_note = RecipeNote.objects.create(
            recipe = self.recipe,
            note_text = 'This is a note about the test recipe'
        )
        self.recipe_tag = RecipeTag.objects.create(
            recipe = self.recipe,
            tag = self.tag
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            ingredient = self.ingredient,
            recipe = self.recipe,
            quantity_amount = 5,
            quantity_unit = 'test units'
        )

    def test_create_ingredient(self):
        url = reverse('ingredient-list')
        ingredient_data = {
            "name": "test ingredient",
            'description': 'description of test ingredient'
        }
        response = self.client.post(url, ingredient_data, format='json')
        self.assertEqual(201, response.status_code)

    def test_create_tag(self):
        url = reverse('tag-list')
        tag_data = {
                "tag_text": "test tag"
            }
        response = self.client.post(url, tag_data, format='json')
        self.assertEqual(201, response.status_code)

    def test_create_blank_recipe(self):
        recipe_data = {
            "title": "TestRecipe",
            "author": self.profile.id,
            "tags": []
        }
        url = reverse('recipe-list')
        response = self.client.post(url, recipe_data, format='json')
        self.assertEqual(201, response.status_code)
    
    def test_create_recipe_with_tags(self):
        url = reverse('recipe-list')
        recipe_data = {
            "title": "TestRecipe",
            "author": self.profile.id,
            "tags": [
                {
                    "tag_text": "test tag1"
                },
                {
                    "tag_text": "test tag2"
                }
            ]
        }

        response = self.client.post(url, recipe_data, format='json')
        self.assertEqual(201, response.status_code)
    
    def test_add_recipe_ingredient(self):
        recipe_ingredient_data = {
            "recipe": self.recipe.id,
            "ingredient": {
                "name": "ingredient X"
            },
            "quantity_amount": "2",
            "quantity_unit": "grams"
        }

        kwargs = {'pk': self.recipe.id}
        url = reverse('recipe-ingredients-list', kwargs=kwargs)
        response = self.client.post(url, recipe_ingredient_data, format='json')

        self.assertEqual(201, response.status_code)


class ModifyDeleteTest(APITestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email = 'recipetest@unittest.com',
            username = 'recipeunittest',
            first_name = 'recipe',
            last_name = 'test',
            password = 'password'
        )
        self.profile = UserProfile.objects.create(
            user_account = self.user
        )
        self.tag = Tag.objects.create(
            tag_text = 'Tag test text'
        )
        self.ingredient = Ingredient.objects.create(
            name = 'Test Ingredient',
            description = 'Test description of test ingredient'
        )
        self.recipe = Recipe.objects.create(
            title = 'Test Recipe Title',
            author = self.profile
        )
        self.recipe_step = RecipeStep.objects.create(
            recipe = self.recipe,
            step_number = 1,
            step_text = 'This is the first step'
        )
        self.recipe_note = RecipeNote.objects.create(
            recipe = self.recipe,
            note_text = 'This is a note about the test recipe'
        )
        self.recipe_tag = RecipeTag.objects.create(
            recipe = self.recipe,
            tag = self.tag
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            ingredient = self.ingredient,
            recipe = self.recipe,
            quantity_amount = 5,
            quantity_unit = 'test units'
        )
    
    def test_modify_recipe(self):
        pass

    def test_modify_recipe_ingredient(self):
        pass
