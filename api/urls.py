from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'books', BooksListAPIView, basename='books-list')
router.register(r'add', BooksAddAPIView, basename='add-detail')

urlpatterns = router.urls
#
app_name = 'api'
urlpatterns = [
    path('', include(urlpatterns)),
]
