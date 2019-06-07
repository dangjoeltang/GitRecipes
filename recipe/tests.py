from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import *


class BaseModelsTest(APITestCase):

    def test_create_ingredient(self):
        url = reverse('ingredient-list')
        ingredient_data = {
            "name": "test ingredient",
            'description': 'description of test ingredient'
        }
        response = self.client.post(url, ingredient_data)
        self.assertEqual(201, response.status_code)

    def test_create_tag(self):
        url = reverse('tag-list')
        tag_data = {
                "tag_text": "test tag"
            }
        response = self.client.post(url, tag_data)
        self.assertEqual(201, response.status_code)
