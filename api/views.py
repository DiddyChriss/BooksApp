from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, MultipleChoiceFilter
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *


solo_auth_list = list((x.authors for x in BooksModel.objects.all() if x.authors is not None))
AUTHORS_CHOICES = list(((x, x) for x in solo_auth_list))

solo_date_list = list((x.published_date for x in BooksModel.objects.all() if x.published_date is not None))
DATE_CHOICES = list(((x, x) for x in solo_date_list))

class MultiFilter(FilterSet):
    authors = MultipleChoiceFilter(lookup_expr='icontains', choices=AUTHORS_CHOICES)
    published_date = MultipleChoiceFilter(lookup_expr='icontains', conjoined=True, choices=DATE_CHOICES)

    class Meta:
        model = BooksModel
        fields = [
            'authors',
            'published_date',
        ]


class BooksListAPIView(
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet,):

    queryset = BooksModel.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['published_date', ]
    filterset_class = MultiFilter
    lookup_field = 'book_id'


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class BooksAddAPIView(
                mixins.CreateModelMixin,
                viewsets.GenericViewSet,
                ):
    queryset = BooksUrlModel.objects.all()
    serializer_class = BooksUrlSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            books = BooksUrlModel.objects.get(user=request.user, url=serializer.data['url'])
            books.books_data = serializer.data['books_data']
            books.save()

            for x in serializer.data['books_data']:
                BooksModel.objects.get_or_create(
                    user=request.user,
                    book_id=x[0],
                    title=x[1],
                    authors=x[2],
                    published_date=x[3][:4],
                    categories=x[4],
                    average_rating=x[5],
                    ratings_count=x[6],
                    thumbnail=x[7],
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)