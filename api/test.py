from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from .serializers import *
from .models import *

User = get_user_model()

class GeoDRFAPITestCase(APITestCase):
    def setUp(self):
        self.user = User(username='testone')          # def user
        self.user.set_password('somepassword')
        self.user.save()

        self.books_url_model = BooksUrlModel.objects.create(
            user=self.user,
            url='https://www.googleapis.com/books/v1/volumes?q=war',
            books_data='some books data',

        )

        self.books_model = BooksModel.objects.create(
            user=self.user,
            book_id='iQY3AQAAMAAJ',
            title='book title',
            authors='book title',
            published_date=1999,
            categories='book cat',
            average_rating=3.4,
            ratings_count=4.5,
            thumbnail='some link',

        )

        self.serializer_data = {
            'user': self.user,
            'url': 'https://www.googleapis.com/books/v1/volumes?q=war',
            'books_data': 'some book data',
        }

        self.serializer_book_data = {
            'user': self.user,
            'book_id': 'iQY3AQAAMAAJ',
            'title': 'book title',
            'authors': 'book title',
            'published_date': 1999,
            'categories': 'book cat',
            'average_rating': 3.4,
            'ratings_count': 4.5,
            'thumbnail': 'some link',
        }

        self.serializer = BooksSerializer(instance=self.books_model)
        self.serializer_url = BooksUrlSerializer(instance=self.books_url_model)



    def test_models_acount(self):                                           # test single models
        books_model = BooksModel.objects.count()
        books_url_model = BooksUrlModel.objects.count()
        user_count = User.objects.count()
        self.assertEqual(books_model, 1)
        self.assertEqual(books_url_model, 1)
        self.assertEqual(user_count, 1)

    def test_get_list(self):                                                # test list of items
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')   # authorization
        data = {
            'url': self.books_url_model.url
        }
        url = api_reverse("api:books-list-list")
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post(self):                                                    # test post
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')   # authorization
        data = {
            'url': 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
        }
        url = api_reverse("api:add-detail-list")
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_serializer(self):
        data = self.serializer_url.data
        self.assertEqual(data['url'], self.serializer_data['url'])
        self.assertEqual(set(data.keys()), set(['user', 'url', 'books_data',]))


