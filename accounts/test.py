from test import *
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from .serializers import *
from .models import *

User = get_user_model()

class AccountDRFAPITestCase(APITestCase):
    def setUp(self):
        self.user = User(id=2, username='testone', email='diddy@diddy.com')          # def user
        self.user.set_password('some_password')
        self.user.save()

        self.serializer_data = {
            'id': 2,
            'username': 'testone',
            'email': 'diddy@diddy.com',
            'password': 'some_password',
            'password2': 'seme_password',
        }

        self.serializer = RegisterSerializer(instance=self.user)

    def test_models_acount(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.serializer_data['username'])
        self.assertEqual(set(data.keys()), set(['id', 'username', 'email',]))

    def test_account_jwt_active_false(self):
        url = reverse('accounts:token_obtain_pair')
        u = User.objects.create_user(username='user', password='pass')
        u.is_active = False
        u.save()
        resp = self.client.post(url, {'username': 'user', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_account_jwt_active_true(self):
        url = reverse('accounts:token_obtain_pair')
        u = User.objects.create_user(username='user', password='pass')
        u.is_active = True
        u.save()
        resp = self.client.post(url, {'username': 'user', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        token = resp.data['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = client.get('/books/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_account_jwt_token_400(self):
        url = reverse('accounts:token_obtain_pair')
        resp = self.client.post(url, {'token': 'abc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_account_jwt_token_401(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer abc')
        resp = client.get('/books/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

