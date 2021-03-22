from django.contrib.auth.models import User
from django.db import models

class BooksUrlModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=1000, null=True)
    books_data = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return str(self.url)


class BooksModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_id = models.CharField(max_length=300, null=True, unique=True)
    title = models.CharField(max_length=300, null=True)
    authors = models.CharField(max_length=300, null=True)
    published_date = models.CharField(max_length=300, null=True)
    categories = models.CharField(max_length=300, null=True)
    average_rating = models.CharField(max_length=300, null=True)
    ratings_count = models.CharField(max_length=300, null=True)
    thumbnail = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.title)
