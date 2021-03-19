import requests
import json

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from .models import *


class BooksUrlSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)
    url = CharField()
    books_data = SerializerMethodField(read_only=True)

    class Meta:
        model = BooksUrlModel
        fields = [
            'user',
            'url',
            'books_data',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_books_data(self, obj):
        try:
            response = requests.get(obj.url, )
            list_of_data = json.loads(response.text)['items']
            items_list = [
                'title',
                'authors',
                'publishedDate',
                'categories',
                'averageRating',
                'ratingsCount',
            ]
            list_of_books = []

            for item in list_of_data:
                list_of_books_parameters = []
                list_of_books_parameters.append(item['id'])
                for x in items_list:
                    try:
                        if isinstance(item['volumeInfo'][x], list):
                            list_of_books_parameters.append(item['volumeInfo'][x][0])
                        else:
                            list_of_books_parameters.append(item['volumeInfo'][x])
                    except:
                        list_of_books_parameters.append(None)

                list_of_books_parameters.append(item['volumeInfo']['imageLinks']['thumbnail'])
                list_of_books.append(list_of_books_parameters)
        except:
            raise serializers.ValidationError('upss, something went wrong with your books data!')
        return list_of_books

    def validate_url(self, value):
        request = self.context.get("request")
        if BooksUrlModel.objects.filter(user=request.user, url=value):
            raise serializers.ValidationError(f"url ({value}) already in use by {request.user}")
        return value


class BooksSerializer(serializers.HyperlinkedModelSerializer):
    user = SerializerMethodField(read_only=True)
    book_id = SerializerMethodField(read_only=True)
    title = SerializerMethodField(read_only=True)
    authors = SerializerMethodField(read_only=True)
    published_date = SerializerMethodField(read_only=True)
    categories = SerializerMethodField(read_only=True)
    average_rating = SerializerMethodField(read_only=True)
    ratings_count = SerializerMethodField(read_only=True)
    thumbnail = SerializerMethodField(read_only=True)

    class Meta:
        model = BooksModel
        fields = [
            'user',
            'book_id',
            'title',
            'authors',
            'published_date',
            'categories',
            'average_rating',
            'ratings_count',
            'thumbnail',
        ]

    lookup_field = 'book_id'
    extra_kwargs = {
        'url': {'lookup_field': 'book_id'}
    }

    def get_user(self, obj):
        return str(obj.user.username)

    def get_book_id(self, obj):
        return obj.book_id

    def get_title(self, obj):
        return obj.title

    def get_authors(self, obj):
        return obj.authors

    def get_published_date(self, obj):
        return int(obj.published_date)

    def get_categories(self, obj):
        return obj.categories

    def get_average_rating(self, obj):
        if obj.ratings_count == None:
            avarage = obj.average_rating
        else:
            avarage = float(obj.average_rating)
        return avarage

    def get_ratings_count(self, obj):
        if obj.ratings_count == None:
            raitings = obj.ratings_count
        else:
            raitings = float(obj.ratings_count)
        return raitings

    def get_thumbnail(self, obj):
        return obj.thumbnail