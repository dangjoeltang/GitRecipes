from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import UserAccount, UserProfile

# Create your tests here.
class UserAccountAPIViewTest(APITestCase):
    url = reverse('account-list')

    def setUp(self):
        UserAccount.objects.create(
            email = 'test@unittest.com',
            username = 'unittest',
            first_name = 'unit',
            last_name = 'test',
            password = 'password'
        )
    
    def test_create_useraccount(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "first_name": 'unit',
            "last_name": 'test'
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_username_unique(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "first_name": 'unit',
            "last_name": 'test'
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "first_name": 'unit',
            "last_name": 'test'
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class JwtTokenTest(APITestCase):
    url = reverse('token_obtain_pair')

    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email = 'test@unittest.com',
            username = 'unittest',
            first_name = 'unit',
            last_name = 'test',
            password = 'password'
        )
        self.user.save()

    def test_token_obtain_valid(self):
        response = self.client.post(self.url, {"username": "unittest", "password": "password"}, format='json')
        self.assertEqual(200, response.status_code)
