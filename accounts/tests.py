from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CreateUserViewTest(APITestCase):
    def test_register_user(self):
        user_data = {
            "username": "test",
            "password1": "secretpassword12345",
            "password2": "secretpassword12345",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "phone_number": "12345678",
            "date_of_birth": "2000-01-01",
            "address": "test"
        }
        response = self.client.post(
            reverse('user-registration'), data=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_password(self):
        # passwords doesn't match
        user_data = {
            "username": "test",
            "password1": "secretpassword12345",
            "password2": "12345",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "phone_number": "12345678",
            "date_of_birth": "2000-01-01",
            "address": "test"
        }
        response = self.client.post(reverse('user-registration'),
                                    data=user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_username_validation(self):
        user_data = {
            "username": "test",
            "password1": "secretpassword12345",
            "password2": "secretpassword12345",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "phone_number": "12345678",
            "date_of_birth": "2000-01-01",
            "address": "test"
        }
        self.client.post(reverse('user-registration'), data=user_data)

        # try to register the same user
        response = self.client.post(
            reverse('user-registration'), data=user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_use_gibberish_email(self):
        user_data = {
            "username": "test",
            "password1": "secretpassword12345",
            "password2": "secretpassword12345",
            "first_name": "test",
            "last_name": "test",
            "email": "wdasdet4rgdftr67@test.com",
            "phone_number": "12345678",
            "date_of_birth": "2000-01-01",
            "address": "test"
        }
        # email hunter find this email as automatically generated email address
        response = self.client.post(
            reverse('user-registration'), data=user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
