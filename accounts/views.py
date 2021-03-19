from django.contrib.auth.models import User
from django.contrib.auth import login

from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from .serializers import *


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data['user']
        user = User.objects.get(username=user_data)
        login(request, user)
        return super(MyObtainTokenPairView, self).post(request, format=None)